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
│ pesquisa       │ │ logo          │ │ arquitetura-  │   revisa TODA peça
│ perguntas-     │ │ identidade-   │ │  site         │   antes de virar
│  iniciais      │ │  visual       │ │ seo           │   "aprovado_interno"
│ briefing       │ │ copy          │ │ dev-web       │
│ dna-marca      │ │ imagens       │ │ performance   │
│ projeto        │ │ posts         │ │ seguranca     │
└────────────────┘ └───────────────┘ └───────────────┘
```

## Os 24 funcionários

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
| 19 | `agente-video` | Criação | Diretor de Vídeo e Motion | revisor-marca → diretor-de-criacao |
| 20 | `agente-copydesk` | Qualidade | Copidesque | diretor-de-criacao |
| 21 | `agente-juridico` | Qualidade | Consultor Jurídico | gerente-de-contas |
| 22 | `agente-analytics` | Mídia e Dados | Analista de Dados | diretor-de-tecnologia |
| 23 | `agente-trafego-pago` | Mídia e Dados | Gestor de Tráfego | analytics → gerente-de-contas |
| 24 | `agente-pesquisa` | Descoberta | Analista de Pesquisa | gerente-de-contas |

## Linha do tempo de um projeto completo

```
FASE 0 — DESCOBERTA
  pesquisa (mercado, concorrentes, voz do público, checagem de nome)
    → perguntas-iniciais → briefing → [GATE CLIENTE]
    → seo modo 1 (demanda de busca) → dna-marca → [GATE CLIENTE]

  A pesquisa abre a fila: o questionário só pergunta o que a pesquisa não
  respondeu, e o DNA só é escrito com evidência externa na mesa.

FASE 1 — PLANEJAMENTO
  projeto (escopo + cronograma + orçamento) → [GATE CLIENTE]

FASE 2 — MARCA
  logo → identidade-visual → [GATE CLIENTE]

FASE 3 — WEB
  arquitetura-site → seo (on-page) → dev-web → performance → seguranca → [GATE CLIENTE]

FASE 4 — CONTEÚDO (recorrente)
  copy + imagens + video → posts → copydesk → revisor-marca → [GATE CLIENTE]

FASE 5 — MÍDIA E RESULTADO (recorrente)
  analytics (mede e valida rastreio) → trafego-pago → analytics (lê resultado)
  juridico entra sempre que houver promessa de resultado ou imagem de pessoa
```

`[GATE CLIENTE]` = precisa de `aprovado_cliente`, não basta aprovação interna.

## Cadeias de aprovação (quem carimba, em que ordem)

| Tipo de entregável | Cadeia |
|---|---|
| Texto (copy, posts) | `copydesk` → `revisor-marca` → `diretor-de-criacao` → gerente |
| Visual (logo, identidade, imagens, vídeo) | `revisor-marca` → `diretor-de-criacao` → gerente |
| Técnico (arquitetura, seo, dev, performance) | `diretor-de-tecnologia` → gerente |
| Segurança | `agente-seguranca` tem **veto** — nada sobe com risco alto aberto |
| Mídia paga | `agente-analytics` valida o rastreio → gerente libera a verba |
| Risco jurídico | `agente-juridico` tem **veto** sobre promessa e uso de imagem |
