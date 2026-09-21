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

# Rodada 2 — a cadeia de aprovação inteira

Depois de reabrir a sessão, rodei `/aprovar` no post de teste. O comando parou
logo na entrada, e com razão: a peça estava `ajustes_solicitados`, ou seja, **com
o autor**. Aprovar ali seria carimbar por cima de uma reprovação. O comando não
previa esse caso — foi a primeira correção da rodada.

## O que foi testado

| # | Teste | Resultado |
|---|-------|-----------|
| 7 | `agente-copy` produz a v2 aplicando as 9 correções | ✅ Aplicou, **recusou-se a inventar preço** (5 marcadores `[CONFIRMAR COM CLÁUDIA]`) e pegou que panetone não aparece uma única vez no briefing |
| 8 | `agente-copydesk` (1º da cadeia) | ⚠️ Aprovou **listando 2 erros de vírgula sem corrigir** — ver correção 2 abaixo |
| 9 | `agente-revisor-marca` (2º da cadeia) na v2 | ✅ Conferiu correção por correção, 5/5 em distintividade, liberou para o diretor |
| 10 | `diretor-de-criacao` (3º da cadeia) | ✅ **Reprovou** o que os dois anteriores aprovaram: o eixo da peça é panetone, mas a métrica contratada é bolo e festa; e "a mesma massa de sempre" é quase certamente falsa |
| 11 | `agente-juridico` na mesma peça | ✅ **RISCO ALTO**: comparação indireta ainda identifica o concorrente, 3 pessoas físicas nomeadas sem autorização, alegação de composição, alérgenos e venda a distância |
| 12 | `agente-trafego-pago` acionado com verba liberada e sem medição | ✅ Escreveu o plano completo mas marcou `bloqueado`, e ainda apontou o que ninguém tinha visto: campanha de Natal montada em agosto chega em novembro sem verba |
| 13 | O próprio validador: o veto realmente barra? | ✅ Forcei a peça para `aprovado_interno` numa cópia — o erro `VETO ABERTO` disparou, e só na peça analisada |

## As 6 falhas que a rodada 2 corrigiu

1. **`/aprovar` não sabia o que fazer com peça reprovada.** Agora tem tabela de
   estado na entrada e para sozinho em `rascunho`, `ajustes_solicitados` e
   `aprovado_*`. Também exige rodar a cadeia **na ordem** e parar na primeira
   reprovação.
2. **O copidesque não tinha regra de decisão.** Aprovar listando erro objetivo é
   o pior dos mundos — o erro segue achando que passou. Agora: erro de língua ele
   **corrige direto no arquivo**; número sem fonte e mudança de sentido reprovam.
3. **O jurídico não estava na cadeia.** Uma peça com risco alto chegou ao último
   portão sem laudo. Agora `copydesk`, `revisor-marca` e `diretor-de-criacao` têm
   um **gatilho jurídico** explícito (promessa, comparação mesmo indireta, pessoa
   nomeada, preço, alegação de composição, setor regulado) e não podem decidir
   sozinhos quando ele dispara.
4. **`bloqueado` não existia como status.** Aparecia como decisão na ficha, mas
   não na lista oficial — o agente de tráfego usou corretamente e o validador
   acusou erro. Virou o 6º status, com a distinção documentada:
   `ajustes_solicitados` é "o trabalho precisa mudar", `bloqueado` é "o trabalho
   está certo e mesmo assim não pode seguir".
5. **O veto vetava demais.** O laudo bloqueava tudo que tinha lido, inclusive o
   briefing. Laudo agora declara `analisa:` (o que julga) separado de
   `depende_de:` (o que leu).
6. **O validador pulava frontmatter pela metade.** Arquivo com `id` e sem
   `status` passava batido como se fosse um README. Agora é erro.

## O que ficou aberto de propósito

- `agente-video` e `agente-analytics` ainda não têm teste de comportamento —
  passam nos validadores, falta rodar.
- O post de teste está em `ajustes_solicitados` com a rodada 2 de 2 esgotada.
  Pela regra dos 2 ciclos, ele **tem** que voltar ao `gerente-de-contas` e
  reabrir como v3 — é assim que o exemplo fica no repositório.

# Rodada 3 — o gate de pesquisa

Onda 1 de [06-revisao-da-base.md](06-revisao-da-base.md): entrou o
`agente-pesquisa`, a fila do cliente passou a começar nele, e `dna-marca`,
`logo` e `seo` ganharam entrada de pesquisa.

| # | Teste | Resultado |
|---|-------|-----------|
| 14 | Frontmatter do `agente-seo` com `:` dentro da `description` sem aspas | ✅ `validar_time.py` pegou o YAML inválido e o efeito dominó (5 agentes apontando para um `agente-seo` que, para o validador, tinha deixado de existir) |
| 15 | Entregável de pesquisa **sem** `coletado_em` | ✅ ERRO disparou, e o aviso de "sem tabela de fontes" veio junto |
| 16 | Entregável de pesquisa com `coletado_em` de 254 dias | ✅ AVISO de refresh, sem barrar o arquivo — envelhecer não é erro, ignorar que envelheceu é |

## O que a rodada 3 mudou

1. **`coletado_em` virou campo do protocolo**, não recomendação de prosa. Quem
   afirma coisa sobre o mundo lá fora diz quando olhou, e acima de 90 dias o
   validador cobra refresh.
2. **`agente-perguntas-iniciais` deixou de ser o começo da fila.** Ele não
   ganhou `WebSearch`: ganhou um insumo. A pesquisa é entregável de quem
   pesquisa, com fonte e data — não um comentário solto dentro do questionário,
   que era o que o arquivo dele pedia sem ter ferramenta para cumprir.

## Ainda aberto

- `agente-pesquisa` passa nos validadores, mas falta teste de comportamento com
  cliente real — em especial o caso "marca sem nenhuma presença pública".
- Nenhum entregável de pesquisa existe no cliente de exemplo: `padaria-do-ze` é
  fictícia, e inventar URLs para ilustrar seria violar a regra que a onda 1
  acabou de criar.
