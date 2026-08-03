# Fluxo de Aprovação

## Os 5 estados de um entregável

| status | significa | quem move para o próximo |
|--------|-----------|--------------------------|
| `rascunho` | o agente executor ainda está trabalhando | o próprio executor |
| `em_revisao` | entregue, esperando o aprovador | o aprovador |
| `ajustes_solicitados` | reprovado com motivo escrito | o executor (volta para rascunho) |
| `aprovado_interno` | passou na revisão da KNG | gerente-de-contas |
| `aprovado_cliente` | o cliente assinou embaixo | gerente-de-contas |

Um entregável nunca pula de `rascunho` para `aprovado_interno`.

## Quem aprova o quê

- **Peças de criação** (logo, identidade, copy, imagens, posts)
  → `agente-revisor-marca` (checa aderência ao DNA)
  → `diretor-de-criacao` (checa qualidade e conceito)
  → `gerente-de-contas` (checa aderência ao escopo e prazo)

- **Entregas técnicas** (arquitetura, SEO, código, performance, segurança)
  → `diretor-de-tecnologia` (checa padrão técnico)
  → `gerente-de-contas` (checa escopo e impacto no prazo)
  → `agente-seguranca` tem **poder de veto**: nada vai ao ar com risco crítico aberto.

- **Documentos de descoberta e planejamento** (briefing, DNA, escopo)
  → `gerente-de-contas` → cliente.

## Regra dos 2 ciclos

Um entregável pode voltar como `ajustes_solicitados` no máximo 2 vezes. Na
terceira, o `gerente-de-contas` obrigatoriamente escala para o humano com um
resumo do impasse — nunca fica em loop infinito de revisão.

## Ficha de aprovação

Todo entregável termina com o bloco de `templates/ficha-de-aprovacao.md`
preenchido. É ali que o aprovador escreve o parecer. Sem ficha preenchida, o
entregável está incompleto.
