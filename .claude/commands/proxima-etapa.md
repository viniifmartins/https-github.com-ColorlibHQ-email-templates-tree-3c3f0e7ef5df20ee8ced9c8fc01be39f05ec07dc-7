---
description: O gerente decide e executa o próximo passo do projeto
argument-hint: <slug do cliente>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

Cliente: **$ARGUMENTS**

Aja como `gerente-de-contas`:

1. Leia o estado da pasta e a tabela "quem aciono agora?" do seu próprio arquivo.
2. Confirme que os insumos da próxima etapa estão `aprovado_interno` ou
   `aprovado_cliente`. Se não estiverem, **pare** e diga exatamente o que falta.
3. Escreva o pedido de trabalho usando `templates/pedido-de-trabalho.md`.
4. Acione o agente responsável.
5. Ao receber a entrega, encaminhe para a cadeia de aprovação dele
   (veja `aprovado_por` no frontmatter do agente) — nunca aprove sozinho peça
   criativa nem entrega técnica.
6. Atualize `status.md`.

Se dois agentes independentes puderem trabalhar em paralelo, acione os dois.
