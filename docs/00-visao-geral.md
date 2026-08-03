# Organograma da KNG

```
                        ┌──────────────────────┐
                        │  GERENTE DE CONTAS   │  ← único ponto de contato com o cliente
                        │  (orquestrador)      │
                        └──────────┬───────────┘
                                   │ delega e cobra
        ┌──────────────────┬───────┴────────┬────────────────────┐
        │                  │                │                    │
┌───────▼────────┐ ┌───────▼───────┐ ┌──────▼────────┐ ┌─────────▼────────┐
│  DESCOBERTA    │ │  DIRETOR DE   │ │  DIRETOR DE   │ │ REVISOR DE MARCA │
│                │ │   CRIAÇÃO     │ │  TECNOLOGIA   │ │ (guardião do DNA)│
├────────────────┤ ├───────────────┤ ├───────────────┤ └──────────────────┘
│ perguntas-     │ │ logo          │ │ arquitetura-  │   revisa TODA peça
│  iniciais      │ │ identidade-   │ │  site         │   antes de virar
│ briefing       │ │  visual       │ │ seo           │   "aprovado_interno"
│ dna-marca      │ │ copy          │ │ dev-web       │
│ projeto        │ │ imagens       │ │ performance   │
│                │ │ posts         │ │ seguranca     │
└────────────────┘ └───────────────┘ └───────────────┘
```

## Os 18 funcionários

| # | Agente | Departamento | Cargo | Aprovado por |
|---|--------|--------------|-------|--------------|
| 1 | `gerente-de-contas` | Atendimento | Gerente de Contas | Cliente (humano) |
| 2 | `diretor-de-criacao` | Criação | Diretor de Criação | gerente-de-contas |
| 3 | `diretor-de-tecnologia` | Tecnologia | Diretor de Tecnologia | gerente-de-contas |
| 4 | `agente-perguntas-iniciais` | Descoberta | Analista de Onboarding | gerente-de-contas |
| 5 | `agente-briefing` | Descoberta | Redator de Briefing | gerente-de-contas |
| 6 | `agente-dna-marca` | Descoberta | Estrategista de Marca | diretor-de-criacao |
| 7 | `agente-projeto` | Planejamento | Gerente de Projeto | gerente-de-contas |
| 8 | `agente-logo` | Criação | Designer de Logo | diretor-de-criacao |
| 9 | `agente-identidade-visual` | Criação | Designer de Identidade | diretor-de-criacao |
| 10 | `agente-copy` | Criação | Redator Publicitário | diretor-de-criacao |
| 11 | `agente-imagens` | Criação | Diretor de Arte / Imagens | diretor-de-criacao |
| 12 | `agente-posts` | Criação | Social Media | diretor-de-criacao |
| 13 | `agente-arquitetura-site` | Tecnologia | Arquiteto de Informação | diretor-de-tecnologia |
| 14 | `agente-seo` | Tecnologia | Especialista em SEO | diretor-de-tecnologia |
| 15 | `agente-dev-web` | Tecnologia | Desenvolvedor Web | diretor-de-tecnologia |
| 16 | `agente-performance` | Tecnologia | Especialista em Performance | diretor-de-tecnologia |
| 17 | `agente-seguranca` | Tecnologia | Especialista em Segurança | diretor-de-tecnologia |
| 18 | `agente-revisor-marca` | Qualidade | Guardião do DNA | diretor-de-criacao |

## Linha do tempo de um projeto completo

```
FASE 0 — DESCOBERTA
  perguntas-iniciais → briefing → [GATE CLIENTE] → dna-marca → [GATE CLIENTE]

FASE 1 — PLANEJAMENTO
  projeto (escopo + cronograma + orçamento) → [GATE CLIENTE]

FASE 2 — MARCA
  logo → identidade-visual → [GATE CLIENTE]

FASE 3 — WEB
  arquitetura-site → seo (on-page) → dev-web → performance → seguranca → [GATE CLIENTE]

FASE 4 — CONTEÚDO (recorrente)
  copy + imagens → posts → revisor-marca → [GATE CLIENTE]
```

`[GATE CLIENTE]` = precisa de `aprovado_cliente`, não basta aprovação interna.
