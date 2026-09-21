# Agência KNG — Time de Agentes

Estrutura de uma agência inteira operando como time de agentes: cada área tem
seu especialista, ninguém aprova o próprio trabalho, e um **gerente de contas**
coordena tudo e é o único que fala com o cliente.

## O que tem aqui

```
CLAUDE.md                    regras globais que todo agente obedece
.claude/agents/              os 23 funcionários (1 arquivo = 1 agente)
.claude/commands/            atalhos: /novo-cliente /status /proxima-etapa /aprovar ...
scripts/validar_time.py      testa a consistência do time (rode antes de commitar)
scripts/validar_entregaveis.py  testa os entregáveis contra o protocolo
scripts/estado.py            gera o estado do escritório para a visualização
docs/00-visao-geral.md       organograma + linha do tempo do projeto
docs/01-fluxo-de-aprovacao.md  estados, quem aprova o quê, regra dos 2 ciclos
docs/02-protocolo-de-handoff.md  formato obrigatório de todo entregável
docs/03-como-adicionar-agente.md  como contratar mais gente
docs/04-visualizacao-bonecos.md   como isso vira a tela dos bonecos trabalhando
docs/06-revisao-da-base.md    auditoria da base: o que falta, em ordem de execução
docs/07-motores-vetor-e-logo.md  pesquisa e desenho do motor vetor e do gerador de logo
equipe/time.json             manifesto do time (organograma legível por máquina)
templates/                   briefing, DNA, escopo, ficha de aprovação
clientes/_exemplo/           estrutura padrão de pasta por cliente
```

## O time

**Atendimento** · gerente-de-contas
**Descoberta** · perguntas-iniciais → briefing → dna-marca
**Planejamento** · projeto
**Criação** · diretor-de-criacao · logo · identidade-visual · copy · imagens · posts · video
**Tecnologia** · diretor-de-tecnologia · arquitetura-site · seo · dev-web · performance · seguranca
**Mídia e Dados** · analytics · trafego-pago
**Qualidade** · revisor-marca (DNA) · copydesk (língua) · juridico (risco)

## Atalhos

| Comando | O que faz |
|---------|-----------|
| `/novo-cliente Padaria do Zé` | cria a pasta, o painel e inicia a descoberta |
| `/status padaria-do-ze` | mostra o que está pronto, parado e com quem |
| `/proxima-etapa padaria-do-ze` | o gerente decide e executa o próximo passo |
| `/aprovar <arquivo>` | roda a cadeia de aprovação do entregável |
| `/relatorio-cliente padaria-do-ze` | escreve o relatório para enviar ao cliente |
| `/auditar-time` | testa a consistência do time e corrige o que achar |

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

1. **Ninguém aprova o próprio trabalho.** Todo agente tem um `aprovado_por`, que
   pode ser uma **cadeia**: um post passa por `copydesk` (língua) →
   `revisor-marca` (DNA) → `diretor-de-criacao` (conceito), nessa ordem — e para
   na primeira reprovação. Promessa, comparação com concorrente ou pessoa
   nomeada acionam o `agente-juridico`, cujo veto vale sobre a cadeia toda.
2. **Tudo vira arquivo com status.** `rascunho → em_revisao → aprovado_interno → aprovado_cliente`.
3. **O DNA da marca é a régua.** Peça que contraria o DNA volta, com o trecho
   violado citado.

## Exemplo real

`clientes/padaria-do-ze/` é um cliente fictício rodado de ponta a ponta na
descoberta — serve de referência de formato e prova que os portões funcionam.

## Testando o time

```bash
python3 scripts/validar_time.py                     # estrutura do time
python3 scripts/validar_entregaveis.py padaria-do-ze  # entregáveis do cliente
python3 scripts/estado.py padaria-do-ze --salvar    # estado do escritório em JSON
```

O que já foi validado rodando o time de verdade está em
[docs/05-teste-do-fluxo.md](docs/05-teste-do-fluxo.md).

O validador checa auto-aprovação, aprovador inexistente, ciclo de chefia,
divergência entre os `.md` e o `time.json`, mesa ocupada por duas pessoas,
agente fora do roteamento e link quebrado na documentação.

## O que falta

A auditoria completa da base está em
[docs/06-revisao-da-base.md](docs/06-revisao-da-base.md): 22 lacunas
priorizadas, com destaque para as três que travam um projeto real hoje — não
existe trilha para o cliente que **já tem logo**, o DNA é escrito sem nenhum
agente com acesso a pesquisa, e a Fase 2 termina em briefing porque **ninguém
produz o vetor final**. O desenho técnico dos dois motores que faltam está em
[docs/07-motores-vetor-e-logo.md](docs/07-motores-vetor-e-logo.md).

## Fase 2

Com o fluxo rodando, `equipe/time.json` + o `status` dos entregáveis alimentam a
visualização dos funcionários trabalhando. Ver `docs/04-visualizacao-bonecos.md`.
