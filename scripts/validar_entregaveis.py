#!/usr/bin/env python3
"""Valida os entregaveis de um cliente contra o Protocolo de Handoff.

Pega o erro que o proprio time encontrou no teste: entregavel marcado como
aprovado sem a ficha de aprovacao preenchida. Tambem checa frontmatter,
dependencias e cadeia de aprovacao.

Uso:  python3 scripts/validar_entregaveis.py [cliente]
      (sem argumento, valida todos os clientes)
"""
import json
import pathlib
import sys

import yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DIR_AGENTES = RAIZ / ".claude" / "agents"
TIME = json.loads((RAIZ / "equipe" / "time.json").read_text(encoding="utf-8"))
# quem revisa (revisor-marca, copydesk, seguranca, juridico) pode, por definicao,
# depender de um entregavel ainda nao aprovado: e exatamente isso que ele analisa.
# quem so escreve parecer dentro da pasta do cliente: controle e lideranca.
# parecer nao e entregavel — nao carrega ficha e pode analisar peca nao aprovada.
REVISORES = {f["id"] for f in TIME["funcionarios"] if f.get("nivel") in ("controle", "lideranca")}
CONTROLE = REVISORES
VETO = {f["id"] for f in TIME["funcionarios"] if f.get("poder_de_veto")}
# marcas de veto no corpo de um laudo
BLOQUEIO = ["RISCO ALTO", "VETADO", "não publicar", "nao publicar"]

STATUS_VALIDOS = ["rascunho", "em_revisao", "ajustes_solicitados", "bloqueado", "aprovado_interno", "aprovado_cliente"]
APROVADOS = ["aprovado_interno", "aprovado_cliente"]
OBRIGATORIOS = ["id", "cliente", "fase", "titulo", "autor", "aprovador", "status", "versao", "data"]

erros: list[str] = []
avisos: list[str] = []


def como_lista(valor) -> list[str]:
    if valor is None:
        return []
    return [str(v) for v in valor] if isinstance(valor, list) else [str(valor)]


def frontmatter(caminho: pathlib.Path) -> tuple[dict, str]:
    texto = caminho.read_text(encoding="utf-8")
    if not texto.startswith("---\n"):
        return {}, texto
    fim = texto.find("\n---\n", 4)
    if fim == -1:
        return {}, texto
    try:
        return yaml.safe_load(texto[4:fim]) or {}, texto[fim + 5 :]
    except yaml.YAMLError as exc:
        erros.append(f"{caminho}: YAML invalido ({exc})")
        return {}, texto


# cadeia de aprovacao declarada por cada agente
cadeias: dict[str, list[str]] = {}
for arquivo in DIR_AGENTES.glob("*.md"):
    front, _ = frontmatter(arquivo)
    if front.get("name"):
        cadeias[front["name"]] = como_lista(front.get("aprovado_por"))

alvo = sys.argv[1] if len(sys.argv) > 1 else None
pastas = [RAIZ / "clientes" / alvo] if alvo else [p for p in (RAIZ / "clientes").iterdir() if p.is_dir()]

total = 0
for pasta in pastas:
    if not pasta.is_dir():
        erros.append(f"cliente nao encontrado: {pasta.name}")
        continue

    ids: dict[str, pathlib.Path] = {}
    docs = []
    for arquivo in sorted(pasta.rglob("*.md")):
        front, corpo = frontmatter(arquivo)
        if not front.get("status"):
            if front.get("id") or front.get("autor"):
                # tem frontmatter de entregavel pela metade: nao pode passar batido
                erros.append(f"{arquivo.relative_to(RAIZ)}: tem 'id'/'autor' mas nao tem 'status'")
                if front.get("id"):
                    ids[front["id"]] = arquivo
            continue  # README, anotacao solta
        docs.append((arquivo, front, corpo))
        if front.get("id"):
            if front["id"] in ids:
                erros.append(f"{arquivo.name}: id '{front['id']}' duplicado (ja usado em {ids[front['id']].name})")
            ids[front["id"]] = arquivo

    # laudos de quem tem veto (juridico, seguranca) que bloqueiam outra peca
    vetos: dict[str, list[str]] = {}
    for arquivo, front, corpo in docs:
        if front.get("autor") in VETO and any(m in corpo for m in BLOQUEIO):
            for alvo in como_lista(front.get("analisa")) or como_lista(front.get("depende_de"))[:1]:
                vetos.setdefault(alvo, []).append(f"{front.get('id')} ({arquivo.name})")

    for arquivo, front, corpo in docs:
        total += 1
        rel = arquivo.relative_to(RAIZ)

        for campo in OBRIGATORIOS:
            if not front.get(campo):
                erros.append(f"{rel}: falta '{campo}' no frontmatter")

        status = str(front.get("status", ""))
        if status not in STATUS_VALIDOS:
            erros.append(f"{rel}: status '{status}' invalido (use um de {STATUS_VALIDOS})")

        autor = front.get("autor")
        if autor and autor not in cadeias:
            erros.append(f"{rel}: autor '{autor}' nao e um agente do time")

        # 'aprovador' pode vir como agente unico ou como a cadeia inteira
        aprovadores = como_lista(front.get("aprovador"))
        for aprovador in aprovadores:
            if aprovador not in cadeias and aprovador != "gerente-de-contas":
                erros.append(f"{rel}: aprovador '{aprovador}' nao e um agente do time")
            if autor and autor == aprovador:
                erros.append(f"{rel}: AUTO-APROVACAO — autor e aprovador sao o mesmo agente")

        cadeia = cadeias.get(autor or "", [])
        if cadeia and aprovadores:
            if len(aprovadores) > 1 and aprovadores != cadeia:
                erros.append(
                    f"{rel}: cadeia no frontmatter ({' -> '.join(aprovadores)}) difere da declarada por {autor} ({' -> '.join(cadeia)})"
                )
            elif len(aprovadores) == 1 and aprovadores[0] != cadeia[0]:
                avisos.append(
                    f"{rel}: aprovador '{aprovadores[0]}' nao e o primeiro da cadeia de {autor} ({' -> '.join(cadeia)})"
                )

        # veto de juridico/seguranca vale sobre toda a cadeia
        if front.get("id") in vetos and status in APROVADOS:
            erros.append(
                f"{rel}: VETO ABERTO — aprovado apesar do laudo {', '.join(vetos[front['id']])}"
            )
        elif front.get("id") in vetos and status not in ("ajustes_solicitados", "rascunho"):
            avisos.append(
                f"{rel}: tem laudo de bloqueio ({', '.join(vetos[front['id']])}) e status '{status}' — deveria voltar ao autor"
            )

        # a brecha encontrada no teste: aprovado com ficha em branco
        if status in APROVADOS and autor not in REVISORES:
            if "Ficha de Aprovação" not in corpo:
                erros.append(f"{rel}: status '{status}' sem Ficha de Aprovacao no arquivo")
            elif not any(marca in corpo for marca in ("[x]", "☑", "**Decisão:** aprovado", "Decisão: aprovado")):
                erros.append(f"{rel}: status '{status}' com a Ficha de Aprovacao EM BRANCO — ninguem carimbou")
            if status == "aprovado_cliente" and "aprovado_cliente" not in corpo:
                avisos.append(f"{rel}: aprovado_cliente sem registro de quem aprovou e quando, na ficha")

        for dep in como_lista(front.get("depende_de")):
            if dep not in ids:
                avisos.append(f"{rel}: depende_de '{dep}' nao encontrado na pasta do cliente")
            else:
                dep_front, _ = frontmatter(ids[dep])
                if (
                    str(dep_front.get("status")) not in APROVADOS
                    and status not in ("rascunho", "bloqueado")
                    and autor not in REVISORES
                ):
                    erros.append(
                        f"{rel}: FILA FURADA — depende de '{dep}', que esta '{dep_front.get('status')}'"
                    )

print(f"Entregaveis verificados: {total}")
for msg in avisos:
    print(f"AVISO: {msg}")
for msg in erros:
    print(f"ERRO:  {msg}")
print(f"\n{len(erros)} erro(s), {len(avisos)} aviso(s)")
sys.exit(1 if erros else 0)
