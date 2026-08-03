# Fluxo de Aprovação

## Os 5 estados de um entregável

| status | significa | quem move para o próximo |
|--------|-----------|--------------------------|
| `rascunho` | o agente executor ainda está trabalhando | o próprio executor |
| `em_revisao` | entregue, esperando o aprovador | o aprovador |
| `ajustes_solicitados` | reprovado com motivo escrito — o **trabalho** precisa mudar | o executor (volta para rascunho) |
| `bloqueado` | o trabalho pode estar certo, mas **não pode seguir**: falta insumo de terceiro, há veto do jurídico ou da segurança, ou uma dependência não foi aprovada | quem destrava a causa (cliente, outro agente, o gerente) |
| `aprovado_interno` | passou na revisão da KNG | gerente-de-contas |
| `aprovado_cliente` | o cliente assinou embaixo | gerente-de-contas |

Um entregável nunca pula de `rascunho` para `aprovado_interno`.

**`ajustes_solicitados` × `bloqueado`** — a diferença importa para saber a quem
cobrar. "Reescreva a headline" é `ajustes_solicitados` e a bola está com o
executor. "O plano está pronto, mas não existe medição instalada e a capacidade
da cozinha é desconhecida" é `bloqueado`: o executor fez a parte dele, quem
destrava é outro.

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
