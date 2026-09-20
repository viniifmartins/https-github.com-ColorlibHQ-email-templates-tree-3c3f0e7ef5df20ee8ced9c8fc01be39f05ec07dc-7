---
id: KNG-INT-DT-02
cliente: kng
fase: docs
titulo: Motor de Geração da KNG — arquitetura, fluxo e regra operacional
autor: diretor-de-tecnologia
aprovador: gerente-de-contas
status: em_revisao
versao: v1
data: 2026-09-20
depende_de: [KNG-INT-SEG-01]
---

# Motor de Geração da KNG

Base de decisão: [`parecer-seguranca-motor-de-geracao.md`](parecer-seguranca-motor-de-geracao.md)
(`KNG-INT-SEG-01`, `aprovado_interno`) e o meu parecer
[`parecer-dt-motor-de-geracao.md`](parecer-dt-motor-de-geracao.md) (`KNG-INT-DT-01`).

## 0. O problema, com a prova na mesa

O material oficial da Higgsfield se divide em duas metades que não se encaixam:

| | Capacidade | Auditabilidade | Custo de construção |
|---|---|---|---|
| **SDK** (`higgsfield-js`, MIT, 2 deps) | só chamada crua de modelo | total — código TypeScript legível | alto: brandkit, consistência e orquestração são nossos, do zero |
| **Skills + CLI** | brandbook em PDF/PPTX, consistência de personagem, catálogo de modelos | nenhuma no ponto crítico | baixo: vem pronto |

As 8 skills oficiais declaram `allowed-tools: Bash` (8 de 8) e conduzem todo o
trabalho pelo executável `higgsfield`. O repositório `cli` **não tem código-fonte**
— a raiz tem `LICENSE`, `README.md`, `MODELS.md`, `THIRD-PARTY-NOTICES.txt`,
`demo.png` e `install.sh`; zero arquivo Go. O binário desce pronto das Releases.
Habilitar as skills como vêm é dar Bash a um binário fechado, com as próprias
skills instruindo o agente a instalá-lo sozinho via `curl | sh` com sudo e sem
checksum (achados O-4, O-5 e O-7 do parecer).

**O fato que destrava a escolha, e que não estava no parecer de segurança:**
o acoplamento ao binário está no **texto** das skills, não no tooling.
`skills/higgsfield-brandkit/scripts/brandkit.py` não invoca `higgsfield` em lugar
nenhum — grep por `higgsfield generate`, `"higgsfield"` e `'higgsfield'` dentro de
`higgsfield-brandkit/scripts/` retorna zero. Os únicos subprocessos são
`rsvg-convert` (`brandkit.py:1031`) e ImageMagick (`:1051`), ambos montados como
lista de argumentos, com `check=True` e `timeout`. Paleta, marcas em SVG,
tipografia e brandbook em PDF/PPTX são Python determinístico sob MIT.

Ou seja: a capacidade que eu queria das skills e o binário que eu não quero
**são separáveis**. A escolha "tudo ou nada" era falsa.

## 1. Decisão: híbrido com fronteira no binário

**A KNG adota o SDK `higgsfield-js` como único caminho de chamada à API, e
reaproveita o tooling local determinístico das skills. O binário `higgsfield` não
entra no fluxo de produção, e nenhum agente da KNG recebe `Bash` para chamá-lo.**

Não é meio-termo por covardia. É a fronteira exata onde o risco muda de natureza:
tudo que é código que eu consigo ler entra; o executável opaco fica fora.

**Vai pelo SDK (`@higgsfield/client`, do npm, com lockfile):**

- toda chamada de geração de imagem e vídeo;
- upload de referência;
- consulta de modelo e polling de job;
- credencial por variável de ambiente (`HF_CREDENTIALS`/`HF_KEY`), que é como o
  SDK já se comporta — ele falha explícito com `CredentialsMissedError` se faltar,
  em vez de seguir sem credencial.

Encapsulado num pacote interno, `kng-gen`, com CLI própria (`kng-gen imagem`,
`kng-gen video`, `kng-gen brandbook`). É ele — e só ele — que guarda a chave,
aplica rate limit, redige log e grava o registro de tratamento do art. 37.
É também a recomendação de longo prazo da seção 5 do parecer, antecipada para o
dia um: sem essa camada, a chave se espalha pelas máquinas das pessoas.

**Vem das skills, como código, não como skill:**

- `higgsfield-brandkit/scripts/` (brandkit.py, render_brandbook_pdf.py e
  referências) — vendorizado numa cópia interna sob MIT, com atribuição
  preservada, versão fixada e commit de origem anotado. Ele já é local e já é
  determinístico.
- O **conhecimento** dos `SKILL.md`: estrutura de prompt, parâmetros por modelo,
  ordem de etapas. Isso vira texto nos nossos agentes de criação, não execução de
  binário.

**Fica de fora, por decisão, não por esquecimento:**

- o binário `higgsfield` e o `install.sh`;
- as 8 skills como skills habilitadas (`allowed-tools: Bash`);
- `higgsfield-soul-id` e qualquer treino de identidade facial — a capacidade mais
  vendável do stack é também a única que trata dado biométrico (LGPD art. 11).
  Fora do escopo do motor enquanto não houver consentimento de dado sensível
  documentado por pessoa retratada;
- `cursor-plugin` e o MCP remoto `mcp.higgsfield.ai` — um servidor remoto define do
  outro lado quais ferramentas o nosso agente enxerga, sem pin e sem aviso;
- `wide-trace/open-higgsfield`, vetado.

**O que perdemos:** consistência de personagem (soul-id) e a conveniência de
"pedir e receber". Aceito. Campanha com rosto de pessoa já dependia de autorização
escrita específica; sem o contrato da seção 3.4, esse trabalho não sairia de
qualquer jeito.

**Exceção controlada:** o binário pode ser instalado **por Homebrew**
(`brew install higgsfield-ai/tap/higgsfield`, que fixa `sha256` e versão por
artefato) em uma máquina de laboratório, sem material de cliente, para
experimentação e comparação de modelos. Nunca em máquina que tenha pasta de
cliente montada. `install.sh` é proibido na KNG, sem exceção.

## 2. Encaixe no fluxo de criação

O motor é **ferramenta**, não etapa. Ele não aparece no organograma e não aprova
nada. Entra dentro do trabalho de agentes que já existem em
[`.claude/agents/`](../.claude/agents/), na mesma cadeia de sempre.

```
agente-dna-marca  (aprovado_cliente)
   └─ agente-logo ............... escreve prompts; NÃO executa
        └─ [operador humano roda kng-gen imagem] → estudos de forma
   └─ agente-identidade-visual .. define sistema; NÃO executa
        └─ [operador humano roda kng-gen brandbook] → brandbook
   └─ agente-imagens ............ escreve prompts em bloco; série de 3+
        └─ [operador humano roda kng-gen imagem]
   └─ agente-video .............. roteiro e storyboard
        └─ [operador humano roda kng-gen video]
   └─ agente-revisor-marca → diretor-de-criacao → gerente-de-contas
```

**Quem chama o quê.** Nenhum agente chama o motor. `agente-logo` e
`agente-identidade-visual` têm `tools: Read, Write, Edit, Glob, Grep` — sem `Bash`,
e assim continuam. `agente-imagens` e `agente-video` têm `Bash` no frontmatter;
esse `Bash` fica restrito a `kng-gen` e a utilitários locais de imagem. Quem
dispara a geração é **pessoa**, com a chave no ambiente dela, a partir do prompt
que o agente escreveu em arquivo. Geração é ato faturável e rastreável; não pode
acontecer como efeito colateral de uma conversa.

**O que continua sendo trabalho humano ou de agente, e não muda:**

- diagnóstico de categoria, as três rotas conceituais e a recomendação do
  `agente-logo`;
- a regra que já está escrita lá: **geração de IA é estudo de forma, nunca arquivo
  final — o vetor final é redesenhado**. O motor não altera isso em uma vírgula;
- a definição de "mundo" e "antimundo" do `agente-imagens`, e a exigência de série
  coerente (3+ imagens com mesma luz, paleta e distância focal);
- seleção, descarte e tratamento. O motor produz candidatos, não entregas;
- roteiro e storyboard, antes de qualquer frame.

## 3. Onde o material aterrissa

Conforme [`CLAUDE.md`](../CLAUDE.md):

| Saída | Destino | Observação |
|---|---|---|
| Estudos de forma de logo | `clientes/<cliente>/01-marca/geracao/logo/` | brutos; o `logo.md` cita os arquivos usados |
| Brandbook gerado (PDF/PPTX/SVG) | `clientes/<cliente>/01-marca/` | entrega do `agente-identidade-visual` |
| Imagens de campanha e produto | `clientes/<cliente>/03-criacao/imagens/` | série completa, inclusive descartes |
| Vídeo e motion | `clientes/<cliente>/03-criacao/video/` | |
| Prompt, modelo, seed, parâmetros, custo, data, operador | `clientes/<cliente>/03-criacao/registro-geracao.md` | um por cliente, append-only |
| Registro de tratamento (art. 37) | interno da KNG, fora da pasta do cliente | escrito pelo `kng-gen`, não à mão |

Subpasta `geracao/` separa bruto de entregável: o que veio do motor nunca se
confunde com o que passou por curadoria. Arquivo gerado sem linha correspondente
no `registro-geracao.md` é tratado como arquivo sem procedência e não sobe para
aprovação.

## 4. As condições do parecer viradas em procedimento

Seção 4 do `KNG-INT-SEG-01`, traduzida em quem faz o quê, quando.

**Chave.** Ninguém recebe a chave de produção. O `kng-gen` lê `HF_CREDENTIALS` do
cofre no momento da execução; a chave não é copiada para `.env`, chat, planilha ou
ticket. Uma chave por pessoa e por ambiente. Rotação a cada 90 dias — tarefa
recorrente no calendário do `gerente-de-contas`, não "quando alguém lembrar".
Desligamento de colaborador: revogação no mesmo dia, antes do encerramento do
acesso ao repositório. 2FA obrigatório na conta Higgsfield e no cofre.

**Instalação.** SDK do npm com lockfile versionado; `npm audit` a cada bump, e
nenhum crítico em aberto passa. Binário só por Homebrew, só na máquina de
laboratório. Quem rodar `install.sh` em máquina da KNG gera incidente de segurança,
não bronca informal.

**Portão de material de cliente.** Enquanto os itens 1 a 4 da seção 3.4 do parecer
(DPA com a Higgsfield, cláusula de transferência internacional, aditivo com o
cliente, autorização de uso de imagem) não estiverem assinados, o `kng-gen` opera
em **modo interno**: só material da própria KNG. Operacionalmente: o `kng-gen`
exige `--cliente <slug>` e recusa qualquer slug que não seja `kng` enquanto
`clientes/<cliente>/02-projeto/autorizacao-ia.md` não existir com
`status: aprovado_cliente`. A trava é do programa, não da disciplina de ninguém.

**Lista do que nunca sai.** Antes de enviar, o `kng-gen` bloqueia por padrão e
exige confirmação nominal quando o prompt ou o anexo contiver: rosto ou voz de
pessoa identificável; documento de identificação, dado de saúde, criança ou
adolescente (esses não têm confirmação possível — é recusa seca); material sob
NDA, campanha não lançada, preço não divulgado; credencial, token ou captura de
painel; base de dados, lista de contato ou planilha de lead. Regra prática para o
`agente-imagens` e o `agente-copy`: **pessoa identificável não entra em prompt**.

**Log.** Toda execução grava quem, para qual cliente, qual finalidade, qual modelo
e qual custo. Prompt e URL de mídia **não** vão para log de terceiro — foi
exatamente o que vetou o repositório não-oficial (N-3), e seria incoerente repetir
em casa. No nosso log, prompt fica no `registro-geracao.md` do cliente, sob acesso
da equipe do projeto.

**Reauditoria.** A cada bump maior do SDK, a cada mudança do tooling vendorizado, e
no mínimo a cada 6 meses. Varredura de segredos no histórico completo dos
repositórios no ato da adoção (os clones auditados eram rasos).

**Confirmação de licença.** Prazo de 30 dias para confirmar o MIT do
`higgsfield-js` por escrito com a Higgsfield ou consumir do npm — a tarball
publicada inclui o `LICENSE` que falta no repositório. Consumir do npm já é o
caminho adotado, o que resolve O-1 na prática.

## 5. O que não muda

A cadeia de aprovação continua inteira. Peça gerada por IA passa por
`agente-revisor-marca` e `diretor-de-criacao` exatamente como peça desenhada à
mão, e depois pelo `gerente-de-contas` para ir ao cliente. Nenhuma exceção por
volume, prazo ou "é só um teste".

Mais que isso: peça gerada por IA passa pelo revisor **com mais atenção**, não com
menos. Um modelo produz média — ele foi treinado no que já existe, e é justamente
por isso que tende ao clichê de categoria que o `agente-logo` é obrigado a evitar.
Se o revisor achar que a peça poderia ser de qualquer concorrente, reprova, e o
argumento "mas foi a IA que fez" não é atenuante.

Continuam valendo, sem alteração: o veto do `agente-revisor-marca` contra o DNA da
marca; o gatilho jurídico (promessa, comparação, pessoa nominada, preço, setor
regulado — `RISCO ALTO` bloqueia mesmo com a cadeia toda aprovando); a proibição de
auto-aprovação; e o contato com o cliente exclusivamente pelo `gerente-de-contas`.

Uma adição, essa sim nova: toda peça que foi ao cliente e teve origem em geração
por IA precisa estar identificada no `registro-geracao.md`. Se o cliente perguntar
"isso foi feito por IA?", a resposta tem que estar em arquivo, não na memória de
quem produziu.

## 6. Riscos que assumo, e o gatilho de saída

| Risco | Por que aceito hoje | Gatilho que muda a decisão |
|---|---|---|
| **Dependência de fornecedor único.** Todo o motor fala com uma API que pode mudar preço, encerrar modelo ou fechar. | O `kng-gen` isola a chamada atrás de interface própria; trocar de fornecedor é reescrever um adaptador, não o fluxo. | Mudança incompatível de API sem prazo de depreciação, ou aumento de preço acima de 50% em um ciclo. |
| **Custo variável sem teto natural.** Geração é cobrada por chamada; série de 3+ imagens multiplica rápido. | Teto por projeto configurado no `kng-gen` e custo registrado por execução. | Custo de geração ultrapassar 15% do valor do projeto. |
| **Reimplementar orquestração.** Sem as skills, escrevemos e mantemos o `kng-gen`. É código nosso, é manutenção nossa. | Superfície pequena: chamada de modelo, polling, upload e teto. Semanas, não trimestres. | O `kng-gen` passar de ~1.500 linhas ou exigir alguém dedicado. Aí o custo do "faço eu" superou o risco que ele evitava. |
| **Tooling vendorizado desatualiza.** A cópia interna do brandkit não recebe upstream automático. | É código determinístico e fechado em escopo; brandbook não muda de forma toda semana. | Upstream corrigir falha de segurança no tooling, ou divergir a ponto de o merge ficar caro. |
| **Ficamos sem consistência de personagem.** Concorrente que usa soul-id entrega algo que não entregamos. | Não existe caminho conforme para biometria hoje. Entregar isso sem base legal é passivo, não vantagem. | Contrato assinado com base legal e consentimento por pessoa, mais reavaliação de segurança específica. |
| **Binário nunca auditado.** Fica de fora, mas fica em laboratório. | Sem material de cliente e sem pasta de cliente montada, o alcance é contido. | Qualquer indício de leitura de disco ou tráfego além da API da Higgsfield: remoção imediata de toda máquina. |

**Gatilho para sair do stack inteiro.** Qualquer um destes, isolado, basta:
incidente de vazamento confirmado na Higgsfield envolvendo material de cliente;
recusa de assinar DPA com finalidade limitada e proibição de treinar com o nosso
material; descoberta de uso do nosso conteúdo para treino sem autorização; ou
achado crítico no SDK que não seja corrigido em 30 dias. O plano B já está
nomeado na seção 5 do parecer: motor auto-hospedado, que elimina a transferência
internacional em vez de contratualizá-la. Manter o `kng-gen` como camada própria é
o que torna esse plano B um trabalho de semanas e não um recomeço.

---

## Ficha de Aprovação

| Campo | Valor |
|---|---|
| Entregável | `KNG-INT-DT-02` — Motor de Geração da KNG |
| Executor | `diretor-de-tecnologia` |
| Cadeia | `diretor-de-tecnologia` → `gerente-de-contas` |
| Rodada | 1 de 2 |

### Passagem pela cadeia
Cada aprovador preenche **só a sua linha**, na ordem.

| # | Aprovador | Decisão | Data | Parecer detalhado em |
|---|-----------|---------|------|----------------------|
| 1 | `gerente-de-contas` | ☐ aprovado ☐ ajustes | | |

**Gatilho jurídico:** ☐ não se aplica ☑ acionado — laudo em `[PENDENTE —
agente-juridico: LGPD, transferência internacional e dado biométrico]`
(promessa, comparação, pessoa nomeada, preço, alegação de composição ou setor
regulado. Laudo `RISCO ALTO` bloqueia, mesmo com a cadeia toda aprovando.)

**Decisão final (quem fecha a cadeia):**
☐ aprovado_interno ☐ ajustes_solicitados ☐ bloqueado

**Ajustes obrigatórios:**
1.
2.
3.

**Pendências que travam a PUBLICAÇÃO mas não a aprovação interna:**
- `[CONFIRMAR COM agente-juridico]` — laudo LGPD antes de habilitar o modo cliente.
- `[CONFIRMAR COM gerente-de-contas]` — DPA e aditivos da seção 3.4 do `KNG-INT-SEG-01`.
- `[CONFIRMAR COM Higgsfield]` — licença MIT do `higgsfield-js` por escrito, 30 dias.

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
