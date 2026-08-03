# Agência KNG — Time de Agentes

Estrutura de uma agência inteira operando como time de agentes: cada área tem
seu especialista, ninguém aprova o próprio trabalho, e um **gerente de contas**
coordena tudo e é o único que fala com o cliente.

## O que tem aqui

```
CLAUDE.md                    regras globais que todo agente obedece
.claude/agents/              os 18 funcionários (1 arquivo = 1 agente)
docs/00-visao-geral.md       organograma + linha do tempo do projeto
docs/01-fluxo-de-aprovacao.md  estados, quem aprova o quê, regra dos 2 ciclos
docs/02-protocolo-de-handoff.md  formato obrigatório de todo entregável
docs/03-como-adicionar-agente.md  como contratar mais gente
docs/04-visualizacao-bonecos.md   como isso vira a tela dos bonecos trabalhando
equipe/time.json             manifesto do time (organograma legível por máquina)
templates/                   briefing, DNA, escopo, ficha de aprovação
clientes/_exemplo/           estrutura padrão de pasta por cliente
```

## O time

**Atendimento** · gerente-de-contas
**Descoberta** · perguntas-iniciais → briefing → dna-marca
**Planejamento** · projeto
**Criação** · diretor-de-criacao · logo · identidade-visual · copy · imagens · posts
**Tecnologia** · diretor-de-tecnologia · arquitetura-site · seo · dev-web · performance · seguranca
**Qualidade** · revisor-marca (guardião do DNA, revisa toda peça criativa)

## Como usar

Abra o Claude Code na raiz deste repositório e fale com o gerente:

```
Cliente novo: Padaria do Zé. Quer marca nova e site. Comece.
```

O `gerente-de-contas` cria a pasta do cliente, aciona o
`agente-perguntas-iniciais` e conduz o fluxo. Você também pode chamar um
especialista direto:

```
@agente-seo audite o site do cliente padaria-do-ze
```

## As 3 regras que fazem isso funcionar

1. **Ninguém aprova o próprio trabalho.** Todo agente tem um `aprovado_por`.
2. **Tudo vira arquivo com status.** `rascunho → em_revisao → aprovado_interno → aprovado_cliente`.
3. **O DNA da marca é a régua.** Peça que contraria o DNA volta, com o trecho
   violado citado.

## Fase 2

Com o fluxo rodando, `equipe/time.json` + o `status` dos entregáveis alimentam a
visualização dos funcionários trabalhando. Ver `docs/04-visualizacao-bonecos.md`.
