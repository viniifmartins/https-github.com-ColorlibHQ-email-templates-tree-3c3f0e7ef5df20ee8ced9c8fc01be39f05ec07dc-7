#!/usr/bin/env python3
"""Gera o estado do escritorio da KNG a partir dos entregaveis de um cliente.

Le o frontmatter de todo .md em clientes/<cliente>/ e devolve, para cada
funcionario, o que ele esta fazendo agora. Essa e a alimentacao da visualizacao
dos bonecos (ver docs/04-visualizacao-bonecos.md).

Uso:
    python3 scripts/estado.py <cliente>            # imprime o JSON
    python3 scripts/estado.py <cliente> --salvar   # grava equipe/estado.json
"""
import datetime
import json
import pathlib
import sys

import yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
TIME = json.loads((RAIZ / "equipe" / "time.json").read_text(encoding="utf-8"))

# status do entregavel -> estado do boneco na tela
MAPA = {
    "rascunho": "trabalhando",
    "em_revisao": "em_revisao",
    "ajustes_solicitados": "bloqueado",
    "aprovado_interno": "entregue",
    "aprovado_cliente": "entregue",
}
PESO = ["ocioso", "entregue", "aguardando_insumo", "trabalhando", "em_revisao", "bloqueado"]
# para quem revisa, um parecer com "ajustes_solicitados" significa trabalho FEITO
# (ele reprovou algo), nao trabalho travado.
CONTROLE = {f["id"] for f in TIME["funcionarios"] if f.get("nivel") == "controle"}


def frontmatter(caminho: pathlib.Path) -> dict:
    texto = caminho.read_text(encoding="utf-8")
    if not texto.startswith("---\n"):
        return {}
    fim = texto.find("\n---\n", 4)
    if fim == -1:
        return {}
    try:
        return yaml.safe_load(texto[4:fim]) or {}
    except yaml.YAMLError:
        return {}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    cliente = sys.argv[1]
    pasta = RAIZ / "clientes" / cliente
    if not pasta.is_dir():
        print(f"cliente nao encontrado: {pasta}")
        return 1

    funcionarios = {
        f["id"]: {
            "estado": "ocioso",
            "nome": f["nome"],
            "departamento": f["departamento"],
            "avatar": f.get("avatar", {}),
            "entregavel": None,
            "com": None,
        }
        for f in TIME["funcionarios"]
    }

    entregaveis = []
    for arquivo in sorted(pasta.rglob("*.md")):
        front = frontmatter(arquivo)
        if not front.get("status") or not front.get("autor"):
            continue
        autor = front["autor"]
        status = str(front["status"])
        aprovador = front.get("aprovador")
        entregaveis.append(
            {
                "id": front.get("id"),
                "titulo": front.get("titulo"),
                "arquivo": str(arquivo.relative_to(RAIZ)),
                "autor": autor,
                "aprovador": aprovador,
                "status": status,
                "versao": front.get("versao"),
            }
        )

        estado = MAPA.get(status, "ocioso")
        if autor in CONTROLE and status == "ajustes_solicitados":
            estado = "entregue"
        if autor in funcionarios and PESO.index(estado) > PESO.index(funcionarios[autor]["estado"]):
            funcionarios[autor].update(
                estado=estado, entregavel=front.get("id"), com=aprovador if status == "em_revisao" else None
            )
        # quem esta com a peca na mao para revisar
        if status == "em_revisao" and aprovador in funcionarios:
            if PESO.index("em_revisao") >= PESO.index(funcionarios[aprovador]["estado"]):
                funcionarios[aprovador].update(estado="revisando", entregavel=front.get("id"), com=autor)

    estado = {
        "cliente": cliente,
        "gerado_em": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "departamentos": TIME["departamentos"],
        "funcionarios": funcionarios,
        "entregaveis": entregaveis,
        "resumo": {
            "total": len(entregaveis),
            "aprovado_cliente": sum(1 for e in entregaveis if e["status"] == "aprovado_cliente"),
            "em_revisao": sum(1 for e in entregaveis if e["status"] == "em_revisao"),
            "bloqueado": sum(1 for e in entregaveis if e["status"] == "ajustes_solicitados"),
        },
    }

    saida = json.dumps(estado, ensure_ascii=False, indent=2)
    if "--salvar" in sys.argv:
        destino = RAIZ / "equipe" / "estado.json"
        destino.write_text(saida + "\n", encoding="utf-8")
        print(f"gravado em {destino.relative_to(RAIZ)} — {len(entregaveis)} entregavel(is)")
    else:
        print(saida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
