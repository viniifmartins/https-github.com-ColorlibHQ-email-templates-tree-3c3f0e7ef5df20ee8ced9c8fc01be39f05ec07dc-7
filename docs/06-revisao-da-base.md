# Revisão da base KNG — o que existe, o que falta

Auditoria completa do repositório em 21/09/2026, com foco em uma pergunta:
**a base atual consegue levar um cliente de "chegou" até "logo vetorial final,
design system e sistema visual completo"?**

Resposta curta: **não**. O processo até o briefing e o DNA está sólido; a partir
do logo, a base descreve entregas em vez de produzi-las, e o caso mais comum do
mundo real — o cliente que **já tem** logo — simplesmente não tem trilha.

## 1. Estado atual (o que está bom e deve ser preservado)

| Camada | Situação |
|---|---|
| Regras globais (`CLAUDE.md`) | Íntegras: fila, arquivo, DNA como lei, quem aprova ≠ quem executa |
| Fluxo de aprovação | 6 estados, cadeia ordenada, regra dos 2 ciclos, veto de segurança e jurídico |
| Protocolo de handoff | Frontmatter obrigatório, `analisa:` separado de `depende_de:`, parecer em arquivo próprio |
| Validadores | `validar_time.py` e `validar_entregaveis.py` passam com **0 erro / 0 aviso** nos 23 agentes e 9 entregáveis |
| Prova de conceito | `clientes/padaria-do-ze/` rodado de ponta a ponta na descoberta, com 13 testes documentados em [05-teste-do-fluxo.md](05-teste-do-fluxo.md) |

Isso é a parte difícil de construir e está feita. Nada abaixo propõe refazer.

## 2. A trilha que não existe: o cliente que já tem logo

Hoje o fluxo é linear e assume marca do zero:
`dna-marca → logo → identidade-visual` (ver [00-visao-geral.md](00-visao-geral.md),
Fase 2). Consequência prática, verificável nos arquivos:

- `.claude/agents/agente-logo.md` só sabe **criar** conceito novo. Não existe
  rota "avaliar o que existe".
- `.claude/agents/agente-identidade-visual.md` exige
  `01-marca/logo.md (aprovado_cliente)` como entrada obrigatória. Cliente que
  chega com logo pronto **não tem esse arquivo** — e, pela regra 1 do
  `CLAUDE.md`, o sistema para. A saída hoje seria inventar um `logo.md`
  retroativo, o que é exatamente o tipo de gambiarra que a base foi feita para
  impedir.
- O `gerente-de-contas` tem uma linha de roteamento só: "Escopo aprovado, marca
  a criar → `agente-logo`". Não há "marca existente a diagnosticar".

As três situações que você descreveu precisam ser **três trilhas explícitas**,
decididas por diagnóstico e não por gosto:

| Trilha | Quando | O que muda no fluxo |
|---|---|---|
| **A — Criar** | não existe marca, ou existe só um nome | fluxo atual, do zero |
| **B — Refazer** | existe logo, mas o diagnóstico reprova (conceito, construção ou risco de registro) | precisa de laudo do ativo antigo + plano de transição/migração |
| **C — Evoluir** | existe logo com equity e construção recuperável | não passa pelo `agente-logo` de criação: passa por reconstrução vetorial + extensão do sistema |

A literatura de brand audit é unânime num ponto que a base hoje não respeita:
**diagnosticar antes de redesenhar** — quem redesenha antes de medir queima
verba e, na trilha C, destrói equity acumulado. O instrumento padrão é um
scorecard multicamada (estratégia, identidade verbal, identidade visual,
presença digital, experiência, contexto competitivo), justamente para evitar o
erro de trocar o logo quando o problema é de estratégia.

### Falta, em ordem

1. **`agente-auditoria-marca`** (P0) — novo agente, departamento Criação.
   Entrega `01-marca/diagnostico-marca.md`: inventário de ativos (existe vetor?
   só JPG? qual fonte? licença?), nota por critério (distintividade,
   legibilidade em 16px, versão monocromática, comportamento em negativo,
   construção técnica, aderência ao DNA, risco de colisão de registro),
   equity observável (tempo de uso, reconhecimento, menções), e **recomendação
   fundamentada de trilha A/B/C**. Aprovado por `revisor-marca` →
   `diretor-de-criacao`, nunca por ele mesmo.
2. **Trilha registrada como decisão** (P0) — a trilha escolhida entra no
   `status.md` e é insumo obrigatório do `agente-projeto`, porque muda escopo,
   prazo e preço. Hoje o `agente-projeto` não recebe essa informação.
3. **Inventário de ativos como entregável** (P1) — hoje "Ativos existentes" é
   um bloco de pergunta no questionário
   (`.claude/agents/agente-perguntas-iniciais.md`), não um arquivo verificável.
   Sem ele, ninguém sabe se a trilha C é viável antes de começar.
4. **Plano de transição** (P1) — nas trilhas B e C: o que troca, em que ordem,
   o que fica no ar com a marca antiga, o que precisa de reimpressão. Ninguém
   é dono disso hoje.

## 3. Pesquisa: o DNA hoje é feito no escuro

Este é o furo mais grave da base, e é invisível porque os validadores não
checam ferramenta.

| Agente | Ferramentas declaradas | Consegue pesquisar? |
|---|---|---|
| `agente-perguntas-iniciais` | Read, Write, Edit, Glob | **não** — e o corpo do agente manda "pesquise o que já dá para saber (site, redes…)" |
| `agente-dna-marca` | Read, Write, Edit, Glob, Grep | **não** |
| `agente-logo` | Read, Write, Edit, Glob, Grep | **não** — e o processo exige "liste o clichê visual dos 3 concorrentes" |
| `agente-identidade-visual` | Read, Write, Edit, Glob, Grep | **não** |

Só três agentes têm `WebSearch`/`WebFetch`: `agente-seo`, `agente-juridico` e
`agente-trafego-pago`. Ou seja: **o DNA da marca, que o `CLAUDE.md` chama de
lei, é escrito apenas com o que o cliente falou de si mesmo.** Diagnóstico de
categoria e clichê de concorrente, hoje, é memória do modelo — não pesquisa.

### Falta, em ordem

5. **`agente-pesquisa`** (P0) — novo agente, departamento Descoberta, com
   `WebSearch`, `WebFetch` e `Bash`. Entrega
   `00-descoberta/pesquisa-mercado.md`: categoria e códigos visuais dominantes,
   3–5 concorrentes com evidência (print de posicionamento, preço público,
   tom), **voz do cliente real** extraída de avaliações e comentários (é de onde
   sai vocabulário verdadeiro, não do dono), tendências, e checagem de nome:
   colisão de marca no INPI, domínio e handles. Regra dura: **toda afirmação com
   URL e data de coleta**, ou marcada `[PREMISSA]` como já manda o
   `agente-briefing`.
6. **Pesquisa de demanda antes do DNA** (P0) — hoje o `agente-seo` só entra na
   Fase 3 (`recebe_de: agente-arquitetura-site`). Como você quer SEO avançado
   alimentando o DNA, falta um entregável de fase 00:
   `00-descoberta/demanda-busca.md` — como o público **nomeia o problema**,
   volume e intenção por termo, entidades da categoria, perguntas reais.
   Isso muda vocabulário, posicionamento e território. É o mesmo agente
   (`agente-seo`), com uma segunda entrada e um segundo entregável — não um
   agente novo.
7. **Regra de frescor e fonte no protocolo** (P1) — nenhum template exige
   `fonte:` nem `coletado_em:`. Pesquisa sem data envelhece em silêncio.
   Entra em [02-protocolo-de-handoff.md](02-protocolo-de-handoff.md).
8. **Naming** (P2) — ninguém gera nem testa nome. O `agente-juridico` revisa
   "nome novo", mas não existe quem o proponha. Só vira P0 se a trilha B
   incluir troca de nome.

## 4. Design system: para no `.md`

`agente-identidade-visual` especifica paleta, tipografia, grid, linguagem
gráfica, aplicações e proibições — e está bem escrito. O problema é que a saída
é **prosa**, inclusive os tokens, que hoje são um bloco CSS ilustrativo de três
linhas no fim do arquivo.

9. **Tokens em formato real** (P0) — entregar
   `01-marca/tokens/tokens.json` no formato **DTCG** (Design Tokens Format
   Module 2025.10, primeira versão estável, publicada em out/2025, com adesão de
   Figma, Style Dictionary, Terrazzo, Penpot, Sketch e Tokens Studio) e gerar
   daí CSS/Tailwind/iOS por build, em vez de o `agente-dev-web` redigitar cor à
   mão. Sem isso não existe design system: existe documento sobre design system.
10. **`scripts/validar_design.py`** (P0) — o `agente-identidade-visual` diz
    "contraste WCAG AA não é opcional", mas **nada verifica**. Falta validador
    que leia os tokens e reprove combinação fora de AA (4.5:1 / 3:1) e reporte
    também o **Lc de APCA** como teto de legibilidade. Nota importante: APCA é
    candidato, não norma — o contraste saiu do rascunho do WCAG 3 em 2023 e, em
    abril de 2026, o algoritmo do WCAG 3 segue "a definir". Então: WCAG 2 como
    piso de conformidade, APCA como leitura de qualidade. Nunca o contrário.
11. **Ícones sem especificação** (P1) — hoje ícone é uma linha dentro de
    "linguagem gráfica". Falta o que faz um set parecer um set: grid (24 com
    padding de 2), keyline shapes, stroke único (1.5 ou 2), tratamento de canto,
    alinhamento a pixel, terminais, teste obrigatório em 16px, e entrega como
    sprite SVG + tokens. Cabe como seção obrigatória do
    `agente-identidade-visual` **ou** como `agente-icones` se o volume
    justificar — a regra "um agente, um entregável" de
    [03-como-adicionar-agente.md](03-como-adicionar-agente.md) favorece separar.
12. **Camada generativa (shaders)** (P1) — não existe dono. O `agente-video`
    cobre roteiro, motion e Lottie; ninguém cobre fundo generativo de marca
    (mesh gradient, grain, noise, liquid, god rays) para web. Falta: definir no
    design system a camada como **parâmetros versionados** (não como print),
    mais requisitos que hoje ninguém cobra — fallback estático, respeito a
    `prefers-reduced-motion`, custo de GPU/bateria e peso. O
    `agente-performance` audita Core Web Vitals, mas não tem uma linha sobre
    canvas WebGL.
13. **Nenhuma prova visual** (P1) — todo entregável da base é texto. O
    `diretor-de-criacao` aprova **descrição** de imagem, não imagem. Falta
    regra: peça visual só entra em `em_revisao` acompanhada de render/preview
    versionado.

## 5. Motor vetor e motor de logo: o furo estrutural

`agente-logo.md` termina assim: *"geração de IA é estudo de forma, nunca arquivo
final — o vetor final é redesenhado"*. Correto — e **por quem?** Não existe esse
funcionário. A agência, hoje, não tem como produzir o arquivo final de uma
marca. Toda a Fase 2 termina em briefing.

14. **`agente-vetor` + pipeline determinístico** (P0) — traçado,
    regularização geométrica, limpeza, validação automática e empacotamento de
    variantes. Especificação completa, com as ferramentas pesquisadas e os
    gates, em [07-motores-vetor-e-logo.md](07-motores-vetor-e-logo.md).
15. **Motor gerador de logo** (P0) — as 3 rotas conceituais do `agente-logo`
    continuam valendo; o que falta é o estágio de geração (construção
    paramétrica por código + IA como estudo) e o **filtro automático** antes do
    olho humano. Também em [07-motores-vetor-e-logo.md](07-motores-vetor-e-logo.md).
16. **Proveniência do visual de marca** (P0) — `agente-imagens` já exige
    registrar ferramenta, seed, parâmetros e direitos
    (`03-criacao/imagens/<lote>.md`). O logo, que é o ativo com maior
    consequência jurídica, **não exige nada disso**. Falta o mesmo registro e um
    gate de colisão de registro no `agente-juridico` **antes** de qualquer
    apresentação ao cliente.

## 6. Achados de estrutura (menores, mas cobram juros)

17. **Binário não tem lugar no protocolo** (P0) — o
    [02-protocolo-de-handoff.md](02-protocolo-de-handoff.md) diz "todo
    entregável é um arquivo `.md`". SVG, PNG, `tokens.json` e Lottie não são.
    Sem regra, cada agente inventa uma. Proposta: binário vive em
    `clientes/<cliente>/<fase>/assets/`, sempre com um `.md` de manifesto que
    carrega `id`, `status`, lista de arquivos e hash — assim o
    `validar_entregaveis.py` continua funcionando sem entender formato binário.
18. **Ferramentas incoerentes com a função** (P1) — `agente-logo` e
    `agente-identidade-visual` não têm `Bash`, então não podem rodar o motor
    vetor nem o validador de contraste que o próprio arquivo deles exige. São
    14 agentes sem `Bash` hoje; nesses dois é bug, não escolha.
19. **Ordem das pastas × ordem do fluxo** (P2) — o disco sugere
    `01-marca` antes de `02-projeto`, o fluxo real é
    descoberta → planejamento → marca. Cosmético, mas custa uma leitura errada
    por cliente novo.
20. **Validadores não cobrem o novo terreno** (P1) — `validar_entregaveis.py`
    não conhece manifesto de asset, tokens nem regra dos 2 ciclos;
    `estado.py` não sabe representar um agente "renderizando" ou "vetorizando".
21. **Comandos faltando** (P2) — não existe `/auditar-marca` (a triagem A/B/C)
    nem `/vetorizar`. E `/aprovar` não sabe lidar com entregável que tem asset
    binário anexo.
22. **Dívida de teste declarada** (P1) — `agente-video` e `agente-analytics`
    seguem sem teste de comportamento, e o post do exemplo está em
    `ajustes_solicitados` com os 2 ciclos esgotados, esperando v3. Já está
    registrado em [05-teste-do-fluxo.md](05-teste-do-fluxo.md); continua aberto.

## 7. Ordem de execução recomendada

Não faça tudo junto. A ordem abaixo é escolhida para que cada etapa já entregue
valor sozinha e para não construir visualização de um fluxo não validado — o
mesmo raciocínio de [04-visualizacao-bonecos.md](04-visualizacao-bonecos.md).

| Onda | Entra | Por que primeiro |
|---|---|---|
| **1** | `agente-pesquisa` + `demanda-busca.md` + ferramentas web no `dna-marca` e no `logo` | destrava a qualidade de **tudo** que vem depois; é a mudança mais barata da lista |
| **2** | `agente-auditoria-marca` + trilhas A/B/C no roteamento do gerente e no escopo | é o caso de cliente mais comum e hoje simplesmente trava |
| **3** | `agente-vetor` + regra de asset binário + `validar_design.py` | é o que transforma briefing em arquivo final entregável |
| **4** | motor gerador de logo (construção paramétrica + IA como estudo + filtro automático) | só faz sentido depois que a pesquisa (onda 1) e o motor vetor (onda 3) existem |
| **5** | tokens DTCG + ícones + camada generativa/shaders | sistema completo em cima de uma marca que já existe em vetor |
| **6** | comandos, `estado.py`, testes de comportamento dos agentes novos | fecha a base para a visualização |

Regra que não muda em nenhuma onda: cada agente novo entra com os **cinco
passos** de [03-como-adicionar-agente.md](03-como-adicionar-agente.md)
(arquivo, `time.json`, roteamento do gerente, organograma, validadores em zero)
— e há 49 mesas livres na planta, então layout não é restrição.
