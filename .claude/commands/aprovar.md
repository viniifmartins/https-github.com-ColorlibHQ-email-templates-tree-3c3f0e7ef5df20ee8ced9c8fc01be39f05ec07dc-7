---
description: Roda a cadeia de aprovação de um entregável
argument-hint: <caminho do entregável>
allowed-tools: Read, Write, Edit, Glob, Grep, Agent
---

Entregável: **$ARGUMENTS**

1. Leia o frontmatter e identifique `autor` e `aprovador`.
2. Descubra a cadeia de aprovação no arquivo do agente autor (campo `aprovado_por`).
   A cadeia roda **em ordem**: quem está antes precisa liberar para o próximo ver.
3. Acione cada aprovador da cadeia, um por vez.
4. Preencha a Ficha de Aprovação (`templates/ficha-de-aprovacao.md`) com o
   parecer de cada um.
5. Atualize o `status` no frontmatter:
   - todos aprovaram → `aprovado_interno`
   - alguém reprovou → `ajustes_solicitados`, com a lista numerada do que mudar
6. Registre a rodada. Na 3ª rodada, pare e escale para o humano.

Regra dura: nenhum agente pode aprovar o próprio trabalho. Se o autor aparecer
como aprovador, isso é um bug da estrutura — reporte em vez de aprovar.
