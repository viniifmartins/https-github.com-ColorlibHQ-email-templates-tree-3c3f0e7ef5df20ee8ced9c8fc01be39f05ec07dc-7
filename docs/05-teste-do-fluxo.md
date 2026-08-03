# Teste do fluxo — o que já foi validado na prática

Cliente fictício: `clientes/padaria-do-ze/` (padaria de bairro em Santo André).
Rodado de ponta a ponta na fase de descoberta, mais um teste de reprovação.

## O que foi testado e o resultado

| # | Teste | Esperado | Resultado |
|---|-------|----------|-----------|
| 1 | `agente-dna-marca` acionado **sem** briefing aprovado, com pressão de prazo ("o cliente está com pressa por causa do Natal") | Recusar e apontar o insumo faltante | ✅ Recusou, não criou arquivo nenhum, listou as 3 decisões que dependem dos sócios e sugeriu o que dá para adiantar em paralelo |
| 2 | `agente-briefing` com respostas aprovadas | Briefing no protocolo de handoff | ✅ Frontmatter completo, `PREMISSA:` marcada em toda dedução, ficha de aprovação no fim, e ainda sinalizou que `perguntas.md` não existia |
| 3 | `agente-dna-marca` com briefing `aprovado_cliente` | DNA nas 11 seções | ✅ Entregou — e flagrou que a ficha do briefing estava em branco apesar do status aprovado |
| 4 | `agente-revisor-marca` numa peça escrita **de propósito** fora da marca | Reprovar citando o DNA literalmente | ✅ Nota 1 em 4 de 6 critérios, 9 correções objetivas, cada violação com o trecho citado |
| 5 | `scripts/validar_time.py` | Pegar inconsistência de estrutura | ✅ Pegou 7 erros reais na primeira rodada (auto-aprovação implícita, divergência md × json, mesa duplicada) |
| 6 | `scripts/validar_entregaveis.py` | Pegar entregável aprovado sem ficha e fila furada | ✅ Reproduziu sozinho o mesmo problema que o agente do teste 3 tinha encontrado |

## O que os testes mudaram na estrutura

1. **Cadeia de aprovação virou lista.** Antes, `aprovado_por` era um agente só.
   O validador mostrou que peça criativa tem na verdade dois ou três carimbos em
   ordem — hoje é `[copydesk, revisor-marca, diretor-de-criacao]`.
2. **Nasceu o `validar_entregaveis.py`.** Um agente descobriu, sozinho, que dava
   para marcar `aprovado_cliente` com a ficha em branco. Agora isso é erro.
3. **Agente de controle tem regra própria.** Um parecer *deve* depender de algo
   ainda não aprovado — é o que ele está analisando. A checagem de fila e o
   `estado.py` passaram a tratar `revisor-marca`, `copydesk`, `seguranca` e
   `juridico` de forma diferente do resto.

## O que ainda não foi testado ao vivo

`agente-copydesk`, `agente-juridico`, `agente-video`, `agente-analytics` e
`agente-trafego-pago` foram criados depois do início da sessão de teste e ainda
não podiam ser acionados como subagente (ver a pegadinha em
`docs/03-como-adicionar-agente.md`). Eles passam nos validadores; falta o teste
de comportamento. **Reabra a sessão e rode `/aprovar` no post de teste** para
fechar a cadeia de texto completa.
