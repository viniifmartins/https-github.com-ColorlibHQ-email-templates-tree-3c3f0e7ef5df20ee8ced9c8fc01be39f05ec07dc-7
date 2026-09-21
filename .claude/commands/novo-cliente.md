---
description: Abre a pasta e o painel de um cliente novo e inicia a descoberta
argument-hint: <nome do cliente> [o que ele quer]
allowed-tools: Read, Write, Edit, Glob, Bash, Agent
---

Cliente novo: **$ARGUMENTS**

Aja como `gerente-de-contas`:

1. Converta o nome em slug (`Padaria do Zé` → `padaria-do-ze`).
2. Crie `clientes/<slug>/` com as subpastas padrão de `CLAUDE.md`.
3. Crie `clientes/<slug>/status.md` a partir de `templates/status.md`.
4. Acione o `agente-pesquisa`. **A fila começa aqui, não no questionário**: o
   que é público a agência descobre sozinha, e perguntar isso ao cliente queima
   a primeira impressão.
5. Com a pesquisa aprovada, acione o `agente-perguntas-iniciais` — o
   questionário cobre só o que a pesquisa não respondeu (seção 7 dela).
6. Ao final, mostre: onde estamos, o que precisa do cliente, próximo passo.

Não pule para briefing, marca ou site antes das respostas chegarem.
