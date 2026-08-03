---
description: Roda a cadeia de aprovação de um entregável
argument-hint: <caminho do entregável>
allowed-tools: Read, Write, Edit, Glob, Grep, Agent
---

Entregável: **$ARGUMENTS**

**Antes de tudo, leia o `status` e decida se há o que aprovar:**

| status atual | o que fazer |
|---|---|
| `rascunho` | **Não rode a cadeia.** A peça ainda é do autor. Diga isso e pare. |
| `ajustes_solicitados` | **Não rode a cadeia.** A peça voltou para o autor. Acione o autor para produzir a próxima versão e só então aprove. Aprovar por cima de uma reprovação apaga o parecer de quem reprovou. |
| `em_revisao` | Siga o fluxo abaixo. |
| `aprovado_interno` | Falta só o gate do cliente, se o entregável exigir. Não rode a cadeia interna de novo. |
| `aprovado_cliente` | Nada a fazer. Mudança daqui em diante é nova versão. |

1. Leia o frontmatter e identifique `autor` e `aprovador`.
2. Descubra a cadeia de aprovação no arquivo do agente autor (campo `aprovado_por`).
   A cadeia roda **em ordem**: quem está antes precisa liberar para o próximo ver.
3. Acione cada aprovador da cadeia, **um por vez e na ordem declarada**. Rodar
   fora de ordem desperdiça revisão: não adianta o diretor discutir conceito num
   texto que o copidesque ainda vai mexer. Se alguém reprovar, **pare a cadeia
   ali** — os seguintes não revisam peça reprovada.
4. Preencha a Ficha de Aprovação (`templates/ficha-de-aprovacao.md`) com o
   parecer de cada um.
5. Atualize o `status` no frontmatter:
   - todos aprovaram → `aprovado_interno`
   - alguém reprovou → `ajustes_solicitados`, com a lista numerada do que mudar
6. Registre a rodada. Na 3ª rodada, pare e escale para o humano.
7. Rode `python3 scripts/validar_entregaveis.py <cliente>` ao final. Zero erro
   antes de considerar aprovado.

Se o entregável tiver marcador de pendência em aberto (`[CONFIRMAR COM ...]`,
`[NÃO RESPONDIDO]`, `PREMISSA:` estrutural), ele **não pode** chegar a
`aprovado_cliente` — no máximo `aprovado_interno` com a pendência registrada na
ficha.

Regra dura: nenhum agente pode aprovar o próprio trabalho. Se o autor aparecer
como aprovador, isso é um bug da estrutura — reporte em vez de aprovar.
