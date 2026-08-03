---
description: Testa a consistência do time (agentes, manifesto, docs)
allowed-tools: Bash, Read, Edit
---

Rode `python3 scripts/validar_time.py`.

Para cada ERRO, corrija a causa (não o sintoma) e rode de novo até zerar.
Para cada AVISO, decida: corrigir ou justificar por escrito na resposta.

Depois rode `python3 scripts/estado.py <cliente>` se houver algum cliente ativo,
para conferir que o estado do escritório é gerável.

Ao final, responda em 5 linhas: quantos agentes, quantos erros havia, o que foi
corrigido, o que ficou de propósito.
