---
description: Mostra o painel do cliente — o que está pronto, parado e com quem
argument-hint: <slug do cliente>
allowed-tools: Read, Glob, Grep, Bash
---

Cliente: **$ARGUMENTS**

Leia `clientes/$ARGUMENTS/status.md` e varra todos os `.md` da pasta do cliente.
Para cada entregável, extraia do frontmatter: `id`, `titulo`, `autor`,
`aprovador`, `status`, `versao`.

Responda exatamente neste formato:

```
ONDE ESTAMOS: <uma frase>

PRONTO:        <entregáveis aprovado_cliente>
EM APROVAÇÃO:  <entregáveis em_revisao — e com quem estão parados>
EM PRODUÇÃO:   <entregáveis rascunho — e com quem>
BLOQUEADO:     <o que trava e o que destrava>

PRÓXIMA AÇÃO:  <quem aciono agora e por quê>
ESPERANDO O CLIENTE: <o que depende dele, desde quando>
```

Se `status.md` estiver desatualizado em relação aos arquivos, corrija-o.
