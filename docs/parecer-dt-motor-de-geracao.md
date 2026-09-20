---
id: KNG-INT-DT-01
cliente: kng
fase: docs
titulo: Parecer do Diretor de Tecnologia sobre o Parecer de Segurança — Motor de Geração (Higgsfield)
autor: diretor-de-tecnologia
aprovador: gerente-de-contas
status: em_revisao
versao: v1
data: 2026-09-20
depende_de: []
analisa: [KNG-INT-SEG-01]
---

# Parecer — Diretor de Tecnologia

Peça analisada: [`parecer-seguranca-motor-de-geracao.md`](parecer-seguranca-motor-de-geracao.md)
(`KNG-INT-SEG-01`, autor `agente-seguranca`). Sou o aprovador declarado e o
último da cadeia técnica desse arquivo — assino o `status` do frontmatter dele.

**Decisão:** `aprovado_interno` (mérito), com dois ajustes editoriais obrigatórios
antes de qualquer circulação fora da equipe técnica.

**Bloqueadores:** nenhum para a aprovação interna do parecer. Os bloqueadores
que o parecer levanta (N-1, N-2, N-3, O-5) permanecem em pé e viram regra
operacional em [`06-motor-de-geracao.md`](06-motor-de-geracao.md).

---

## 1. O que eu conferi antes de opinar

Não aprovo documento que não consegui reproduzir. Reexecutei por amostragem as
afirmações estruturais do parecer no mesmo material clonado:

| Afirmação do parecer | Minha verificação | Resultado |
|---|---|---|
| `cli` não tem código-fonte Go | `ls cli/` → `LICENSE`, `README.md`, `MODELS.md`, `THIRD-PARTY-NOTICES.txt`, `demo.png`, `install.sh` | **Confirmado.** Zero arquivo `.go`. |
| Skills dependem do binário | As 8 skills declaram `allowed-tools: Bash` (8/8) e chamam o executável `higgsfield` no corpo do `SKILL.md` | **Confirmado.** |
| `higgsfield-js` é enxuto | 2 dependências de produção; `src/` sem `eval`/`child_process`/`postinstall` | **Confirmado.** |
| `skills` monta subprocesso como lista de argumentos | `brandkit.py:1031` e `:1051` — listas literais (`rsvg-convert`, ImageMagick), `check=True`, `timeout` definido | **Confirmado.** |
| Nenhum segredo versionado | varredura na árvore de trabalho | **Confirmado**, com a ressalva de método que o próprio autor registrou (clones rasos). |

**Achado meu, que o parecer não registrou e que é material para a decisão de
arquitetura:** `skills/higgsfield-brandkit/scripts/brandkit.py` **não invoca o
binário `higgsfield` em momento algum**. Grep por `higgsfield generate`,
`"higgsfield"` e `'higgsfield'` dentro de `higgsfield-brandkit/scripts/` retorna
**zero**. Os únicos subprocessos são `rsvg-convert` e ImageMagick. A dependência
do binário fechado mora no texto do `SKILL.md` (instruções ao agente), não no
tooling local. Isso significa que a parte determinística do brandkit — paleta,
SVG, brandbook em PDF/PPTX — é código Python MIT, auditável, e **separável** do
CLI. É sobre esse achado que construo o motor híbrido no `KNG-INT-DT-02`.

**Divergência menor de contagem, sem efeito na decisão.** O pedido que me chegou
citava 24 ocorrências de `higgsfield generate`, 10 de `higgsfield model` e 4 de
`higgsfield soul-id`. Contando apenas os 8 `skills/higgsfield-*/SKILL.md`, obtive
**42**, **16** e **5**. Contando a árvore inteira de `skills/` (docs, cookbook,
references, evals), **141**, **54** e **10**. Registro porque número citado sem
método é número que ninguém consegue refazer. O fato de fundo — acoplamento total
das skills ao binário — fica **mais** forte, não menos.

---

## 2. Julgamento do item (a) — erro de frontmatter

O parecer está com `analisa: [KNG-INT-SEG-01]`, que aponta para ele mesmo.
Isso é erro, e não é cosmético: o campo `analisa` é o que liga um parecer à peça
revisada. Apontando para si, o documento se declara revisão da própria revisão, e
quem for varrer o repositório por "o que já foi analisado" encontra um laço.

**O que é correto aqui:** o `KNG-INT-SEG-01` **não é um parecer sobre peça da
KNG**. É uma auditoria de repositórios de terceiro — não há entregável KNG do
outro lado. Logo o campo `analisa` não tem alvo legítimo no nosso espaço de `id`s.
O correto é `analisa: []`, com o objeto auditado permanecendo declarado onde já
está e onde é verificável: a tabela "O que foi lido (cópias locais)" da seção 0,
com repositório e caminho. `KNG-INT-SEG-01` é a peça-raiz; quem a analisa é
**este** arquivo, e é por isso que é aqui que `analisa: [KNG-INT-SEG-01]` aparece
corretamente.

**Exijo a correção; não a executo.** Regra da casa: ninguém edita arquivo de outro
agente. O ajuste é do `agente-seguranca`, em `v2`, com changelog no fim do arquivo.

## 3. Julgamento do item (b) — procedência do `wide-trace/open-higgsfield`

O autor classificou como "NÃO VERIFICÁVEL" a data de criação, o número de commits
e a contagem de stars, porque o clone local é raso (1 commit visível). **O método
dele está certo**: com clone raso na mão, afirmar "3 commits" seria inventar. Ele
se recusou a usar como fundamento algo que não podia provar, e ainda corrigiu um
achado preliminar falso seu (o log do blob). Isso é o comportamento que eu quero
ver num parecer de segurança e é metade da razão de eu aprovar este documento.

O limite, porém, era de **fonte**, não de realidade. Os dados foram obtidos por
fonte primária nesta sessão — **API do GitHub**, não o clone:

- criação em **2026-08-26**;
- **3 commits**;
- **2.307 stars**, **315 forks**;
- dono `wide-trace`, **sem vínculo** com a organização `higgsfield-ai`.

**Aceito como prova válida de procedência**, com a fonte nomeada. A regra da casa
é prova antes de opinião, e API do provedor é prova de metadado tão boa quanto
código lido em disco é prova de comportamento — desde que a fonte esteja escrita
ao lado do número. Fica a ressalva óbvia: metadado do GitHub descreve o
repositório, não audita o código; não substitui nada da seção 2.

**Muda o fundamento do veto? Não.** E faço questão de que fique assim.
O veto se sustenta em três fatos de código, verificáveis offline, que continuam
intactos: ausência de `LICENSE` (N-1), `POST /api/blob` sem autenticação com o
comentário do próprio autor admitindo (N-2), e prompt e mídia do cliente em log
de servidor em claro (N-3). Nenhum deles depende de quantas stars o repositório
tem. Se amanhã o repo tiver 50 mil stars, segue vetado; se tiver zero, o veto
também não fica "mais forte".

**O que a prova muda, e não é pouco:** a tese de star inflacionada sai de
"suspeita não comprovada" para **anomalia documentada** — 2.307 stars sobre 3
commits em 25 dias, em repositório de dono sem vínculo com a organização cujo
nome ele usa no título. Isso é sinal de risco de cadeia de suprimento e de
confusão de marca deliberada, e vale como **contexto agravante** e como alerta de
processo: alguém do time pode topar com esse repo, ler "Open-Source Alternative"
e "Free", e presumir oficialidade. Por isso vira ajuste obrigatório: o parecer
deve substituir o trecho "NÃO VERIFICÁVEL / suspeita não comprovada" pelos números
com a fonte declarada (API do GitHub, 2026-09-20), e registrar, no veredito de
N-1, que o repositório **não é da Higgsfield** — o que a seção 1 já diz e agora
tem lastro documental.

---

## 4. Ajustes obrigatórios

1. **Frontmatter:** trocar `analisa: [KNG-INT-SEG-01]` por `analisa: []`. O objeto
   auditado são repositórios de terceiro, já declarados na tabela da seção 0.
   Publicar como `v2` com changelog.
2. **Seção 0, limite declarado:** substituir o bullet "Data de criação, número de
   commits e contagem de stars: NÃO VERIFICÁVEL" pelos dados obtidos por fonte
   primária — repositório criado em 2026-08-26, 3 commits, 2.307 stars, 315 forks,
   dono `wide-trace` sem vínculo com `higgsfield-ai` — **com a fonte nomeada
   (API do GitHub, consulta de 2026-09-20)** e com a frase explícita de que isso é
   contexto agravante, **não** fundamento do veto (que segue em N-1, N-2 e N-3).
3. **Seção 2.1:** registrar o achado de que `higgsfield-brandkit/scripts/` não
   invoca o binário fechado — é fato favorável à adoção parcial e o parecer, hoje,
   induz a conclusão oposta (de que capacidade de brandkit implica CLI).

Os itens 1 e 2 são de forma e de registro. Nenhum deles altera veredito, achado ou
severidade — por isso **não travam a aprovação interna**, mas travam a circulação
do documento para fora da equipe técnica (sócio, jurídico, cliente).

## 5. Dívida aceita conscientemente

- **Comportamento do binário do CLI em runtime: não auditado.** Aceito enquanto o
  binário não receber material de cliente e a instalação for por Homebrew com
  `sha256`. Detalhado como procedimento no `KNG-INT-DT-02`.
- **Varredura de segredos no histórico completo:** pendente, clones rasos. Prazo:
  no ato da adoção, como o autor já registrou.
- **Retenção de dados do lado da Higgsfield:** insolúvel por código. Só contrato.
  Fica travando a entrada de material de cliente, conforme seção 3.4 do parecer.

## 6. O que eu não mexi

Não editei `parecer-seguranca-motor-de-geracao.md` a não ser na **minha** linha da
Ficha de Aprovação e no `status` do frontmatter — que é atribuição minha por ser o
último da cadeia. Nenhum campo de outro aprovador foi preenchido.

---

## Ficha de Aprovação

| Campo | Valor |
|---|---|
| Entregável | `KNG-INT-DT-01` — Parecer do Diretor de Tecnologia sobre `KNG-INT-SEG-01` |
| Executor | `diretor-de-tecnologia` |
| Cadeia | `diretor-de-tecnologia` → `gerente-de-contas` |
| Rodada | 1 de 2 |

### Passagem pela cadeia
Cada aprovador preenche **só a sua linha**, na ordem.

| # | Aprovador | Decisão | Data | Parecer detalhado em |
|---|-----------|---------|------|----------------------|
| 1 | `gerente-de-contas` | ☐ aprovado ☐ ajustes | | |

**Gatilho jurídico:** ☐ não se aplica ☑ acionado — laudo em `[PENDENTE — LGPD,
seção 3 de KNG-INT-SEG-01: transferência internacional e dado biométrico]`
(promessa, comparação, pessoa nomeada, preço, alegação de composição ou setor
regulado. Laudo `RISCO ALTO` bloqueia, mesmo com a cadeia toda aprovando.)

**Decisão final (quem fecha a cadeia):**
☐ aprovado_interno ☐ ajustes_solicitados ☐ bloqueado

**Ajustes obrigatórios:**
1.
2.
3.

**Pendências que travam a PUBLICAÇÃO mas não a aprovação interna:**
- `[CONFIRMAR COM agente-juridico]` — laudo sobre transferência internacional e
  base legal para dado biométrico, antes de qualquer uso com material de cliente.

**Aderência ao DNA (preenchido pelo `agente-revisor-marca`):**
| Critério | Nota (1-5) | Observação |
|---|---|---|
| Propósito | | |
| Posicionamento | | |
| Tom de voz | | |
| Público | | |
| Consistência visual | | |
| Distintividade | | |

**Aprovação do cliente:** ☐ aprovado_cliente — data: ____ — quem: ____
