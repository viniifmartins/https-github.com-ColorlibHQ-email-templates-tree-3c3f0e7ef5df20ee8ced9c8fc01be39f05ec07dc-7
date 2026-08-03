#!/usr/bin/env python3
"""Valida a consistencia do time da KNG.

Checa que os arquivos de agente, o manifesto equipe/time.json e a documentacao
contam a mesma historia. Roda sem dependencia externa alem de pyyaml.

Uso:  python3 scripts/validar_time.py
Saida: lista de ERRO/AVISO. Codigo 1 se houver ERRO.
"""
import json
import pathlib
import re
import sys
import unicodedata

import yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DIR_AGENTES = RAIZ / ".claude" / "agents"
TIME_JSON = RAIZ / "equipe" / "time.json"
GERENTE = "gerente-de-contas"

# destinos que nao sao agentes, mas sao validos em recebe_de/entrega_para
EXTERNOS = {"humano", "cliente", "criacao", "tecnologia"}
CAMPOS_FRONT = ["name", "description", "tools", "model"]
CAMPOS_KNG = ["departamento", "cargo", "reporta_para", "aprovado_por"]
SECOES_OBRIGATORIAS = ["Entradas obrigatórias", "Nunca"]

erros: list[str] = []
avisos: list[str] = []


def erro(msg: str) -> None:
    erros.append(msg)


def aviso(msg: str) -> None:
    avisos.append(msg)


def ler_frontmatter(caminho: pathlib.Path) -> tuple[dict, str]:
    texto = caminho.read_text(encoding="utf-8")
    if not texto.startswith("---\n"):
        erro(f"{caminho.name}: nao comeca com frontmatter '---'")
        return {}, texto
    fim = texto.find("\n---\n", 4)
    if fim == -1:
        erro(f"{caminho.name}: frontmatter nao fechado")
        return {}, texto
    try:
        dados = yaml.safe_load(texto[4:fim]) or {}
    except yaml.YAMLError as exc:
        erro(f"{caminho.name}: YAML invalido no frontmatter ({exc})")
        return {}, texto
    return dados, texto[fim + 5 :]


def slug(texto: str) -> str:
    """criação -> criacao, para comparar rotulo humano com id de departamento."""
    sem_acento = unicodedata.normalize("NFKD", str(texto))
    return "".join(c for c in sem_acento if not unicodedata.combining(c)).strip().lower()


def como_lista(valor) -> list[str]:
    if valor is None:
        return []
    if isinstance(valor, list):
        return [str(v) for v in valor]
    return [str(valor)]


# ---------------------------------------------------------------- carregar
if not DIR_AGENTES.is_dir():
    erro(f"pasta de agentes nao encontrada: {DIR_AGENTES}")
    print("ERRO:", erros[0])
    sys.exit(1)

agentes: dict[str, dict] = {}
corpos: dict[str, str] = {}
for arquivo in sorted(DIR_AGENTES.glob("*.md")):
    front, corpo = ler_frontmatter(arquivo)
    if not front:
        continue
    nome = front.get("name", "")
    if nome != arquivo.stem:
        erro(f"{arquivo.name}: campo name='{nome}' difere do nome do arquivo '{arquivo.stem}'")
    agentes[nome or arquivo.stem] = front
    corpos[nome or arquivo.stem] = corpo

conhecidos = set(agentes) | EXTERNOS

# ------------------------------------------------------- checagens por agente
for nome, front in agentes.items():
    for campo in CAMPOS_FRONT + CAMPOS_KNG:
        if campo not in front:
            erro(f"{nome}: falta o campo obrigatorio '{campo}' no frontmatter")

    desc = str(front.get("description", ""))
    if len(desc) < 60:
        aviso(f"{nome}: description curta demais ({len(desc)} chars) — o gerente pode nao saber quando delegar")
    if len(desc) > 600:
        aviso(f"{nome}: description longa demais ({len(desc)} chars)")
    if "Use " not in desc and "use " not in desc:
        aviso(f"{nome}: description nao diz QUANDO acionar (faltou 'Use quando...')")

    if front.get("model") not in {"opus", "sonnet", "haiku", "inherit"}:
        erro(f"{nome}: model='{front.get('model')}' invalido")

    cadeia = como_lista(front.get("aprovado_por"))
    if not cadeia:
        erro(f"{nome}: sem aprovado_por — todo agente precisa de um aprovador")
    for aprovador in cadeia:
        if aprovador == nome:
            erro(f"{nome}: AUTO-APROVACAO — aprovado_por aponta para ele mesmo")
        if aprovador not in conhecidos:
            erro(f"{nome}: aprovado_por='{aprovador}' nao existe")

    chefe = front.get("reporta_para")
    if chefe == nome:
        erro(f"{nome}: reporta_para aponta para ele mesmo")
    if chefe and chefe not in conhecidos:
        erro(f"{nome}: reporta_para='{chefe}' nao existe")

    for campo in ("recebe_de", "entrega_para"):
        for alvo in como_lista(front.get(campo)):
            if alvo not in conhecidos:
                erro(f"{nome}: {campo}='{alvo}' nao existe")

    for aprovado in como_lista(front.get("aprova")):
        if aprovado in agentes and nome not in como_lista(agentes[aprovado].get("aprovado_por")):
            erro(f"{nome}: declara aprovar '{aprovado}', mas nao esta na cadeia aprovado_por dele")

    corpo = corpos[nome]
    for secao in SECOES_OBRIGATORIAS:
        if secao.lower() not in corpo.lower():
            aviso(f"{nome}: corpo sem a secao '{secao}'")

# ------------------------------------------------- ciclos na cadeia de chefia
for nome in agentes:
    visto, atual = [], nome
    while atual and atual in agentes:
        if atual in visto:
            erro(f"ciclo em reporta_para: {' -> '.join(visto + [atual])}")
            break
        visto.append(atual)
        atual = agentes[atual].get("reporta_para")

# ------------------------------------------------- coerencia com o time.json
if not TIME_JSON.is_file():
    erro("equipe/time.json nao encontrado")
    time = {}
else:
    try:
        time = json.loads(TIME_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        erro(f"equipe/time.json: JSON invalido ({exc})")
        time = {}

if time:
    deps = {d["id"] for d in time.get("departamentos", [])}
    no_json = {f["id"]: f for f in time.get("funcionarios", [])}

    for faltando in sorted(set(agentes) - set(no_json)):
        erro(f"{faltando}: existe em .claude/agents/ mas nao esta em equipe/time.json")
    for sobrando in sorted(set(no_json) - set(agentes)):
        erro(f"{sobrando}: esta em equipe/time.json mas nao existe em .claude/agents/")

    for ident, func in no_json.items():
        front = agentes.get(ident)
        if not front:
            continue
        dep_json = func.get("departamento")
        if dep_json not in deps:
            erro(f"{ident}: departamento '{dep_json}' nao existe na lista de departamentos")
        dep_md = slug(front.get("departamento", ""))
        if dep_json and dep_md and slug(dep_json) != dep_md:
            erro(f"{ident}: departamento diverge — md='{dep_md}' json='{dep_json}'")
        if como_lista(func.get("aprovado_por")) != como_lista(front.get("aprovado_por")):
            erro(f"{ident}: aprovado_por diverge — md='{front.get('aprovado_por')}' json='{func.get('aprovado_por')}'")
        if func.get("modelo") != front.get("model"):
            erro(f"{ident}: modelo diverge — md='{front.get('model')}' json='{func.get('modelo')}'")
        if func.get("reporta_para") != front.get("reporta_para"):
            erro(f"{ident}: reporta_para diverge — md='{front.get('reporta_para')}' json='{func.get('reporta_para')}'")
        caminho = RAIZ / func.get("arquivo", "")
        if not caminho.is_file():
            erro(f"{ident}: arquivo '{func.get('arquivo')}' apontado no time.json nao existe")
        mesa = func.get("avatar", {}).get("mesa")
        if not (isinstance(mesa, list) and len(mesa) == 2):
            erro(f"{ident}: avatar.mesa invalido (esperado [coluna, linha])")

    # duas pessoas na mesma mesa
    mesas: dict[tuple, list[str]] = {}
    for ident, func in no_json.items():
        mesa = func.get("avatar", {}).get("mesa")
        if isinstance(mesa, list) and len(mesa) == 2:
            mesas.setdefault(tuple(mesa), []).append(ident)
    for mesa, gente in mesas.items():
        if len(gente) > 1:
            erro(f"mesa {list(mesa)} ocupada por mais de um funcionario: {', '.join(gente)}")

    # simetria aprova <-> aprovado_por
    for ident, func in no_json.items():
        for aprovado in func.get("aprova", []):
            if aprovado in no_json and ident not in como_lista(no_json[aprovado].get("aprovado_por")):
                erro(f"{ident}.aprova inclui '{aprovado}', mas ele nao esta na cadeia aprovado_por de {aprovado}")

    # todo agente citado em alguma fase
    em_fases = {a for f in time.get("fases", []) for a in f.get("agentes", [])}
    for ident, func in no_json.items():
        if func.get("nivel") == "especialista" and ident not in em_fases:
            aviso(f"{ident}: especialista fora de qualquer fase em time.json")

# ------------------------------------------- roteamento do gerente de contas
corpo_gerente = corpos.get(GERENTE, "")
for ident, front in agentes.items():
    if ident == GERENTE or front.get("nivel") == "lideranca":
        continue
    if ident not in corpo_gerente and ident not in (RAIZ / "docs" / "00-visao-geral.md").read_text(encoding="utf-8"):
        aviso(f"{ident}: nao aparece no roteamento do gerente-de-contas nem no organograma")

# ------------------------------------------------------- referencias de docs
for arquivo in list(RAIZ.glob("*.md")) + list((RAIZ / "docs").glob("*.md")):
    for alvo in re.findall(r"\]\(([^)#][^)]*)\)", arquivo.read_text(encoding="utf-8")):
        if alvo.startswith(("http", "mailto")):
            continue
        if not (arquivo.parent / alvo).exists() and not (RAIZ / alvo).exists():
            erro(f"{arquivo.relative_to(RAIZ)}: link quebrado para '{alvo}'")

# -------------------------------------------------------------------- saida
print(f"Agentes encontrados: {len(agentes)}")
for msg in avisos:
    print(f"AVISO: {msg}")
for msg in erros:
    print(f"ERRO:  {msg}")
print(f"\n{len(erros)} erro(s), {len(avisos)} aviso(s)")
sys.exit(1 if erros else 0)
