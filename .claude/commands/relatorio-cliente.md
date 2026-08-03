---
description: Escreve o relatório de status para enviar ao cliente
argument-hint: <slug do cliente>
allowed-tools: Read, Glob, Grep, Write
---

Cliente: **$ARGUMENTS**

Aja como `gerente-de-contas` falando **com o cliente** — pt-BR claro, sem jargão
de agência, sem nome de agente interno.

Estrutura obrigatória:

1. **O que entregamos** desde o último relatório (só o que está `aprovado_interno`
   ou acima — nunca mostre rascunho).
2. **O que precisamos de você**, com prazo e o impacto de atrasar.
3. **O que vem depois**, com data.
4. **Resultados**, quando houver medição do `agente-analytics` — número, período
   de comparação e leitura em uma frase.

Nunca prometa prazo que não está no cronograma de `02-projeto/escopo.md`.
Salve em `clientes/$ARGUMENTS/relatorios/<AAAA-MM-DD>.md`.
