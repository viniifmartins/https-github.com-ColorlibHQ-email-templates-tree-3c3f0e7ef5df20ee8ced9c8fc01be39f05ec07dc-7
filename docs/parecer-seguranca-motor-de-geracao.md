---
id: KNG-INT-SEG-01
cliente: kng
fase: docs
titulo: Parecer de Segurança — Motor de Geração de Logo, Imagem e Vídeo (Higgsfield)
autor: agente-seguranca
aprovador: diretor-de-tecnologia
status: em_revisao
versao: v1
data: 2026-09-20
depende_de: []
analisa: [KNG-INT-SEG-01]
---

# Parecer de Segurança — Motor de Geração (stack Higgsfield)

## 0. Escopo, método e limites

**O que é:** auditoria de ferramental interno da KNG. Não é peça de cliente e não
é teste ofensivo — é **revisão defensiva de código-fonte de terceiro já clonado
localmente**. Nenhum sistema de terceiro foi sondado, nenhuma requisição foi
disparada contra a API da Higgsfield. Por isso não se aplica a exigência de
autorização escrita de cliente em `02-projeto/`.

**O que foi lido (cópias locais):**

| Repositório | Caminho auditado |
|---|---|
| `wide-trace/open-higgsfield` (NÃO-oficial) | `/home/user/wide-trace/open-higgsfield` |
| `higgsfield-ai/higgsfield-js` | `.../scratchpad/hf/higgsfield-js` |
| `higgsfield-ai/higgsfield-client` | `.../scratchpad/hf/higgsfield-client` |
| `higgsfield-ai/cli` | `.../scratchpad/hf/cli` |
| `higgsfield-ai/skills` | `.../scratchpad/hf/skills` |
| `higgsfield-ai/cursor-plugin` | `.../scratchpad/hf/cursor-plugin` |
| `higgsfield-ai/homebrew-tap` | `.../scratchpad/hf/homebrew-tap` |

(Prefixo completo do scratchpad: `/tmp/claude-0/-home-user-https-github-com-ColorlibHQ-email-templates-tree-3c3f0e7ef5df20ee8ced9c8fc01be39f05ec07dc-7/01ef54b7-f8e1-5ba9-ba68-dfc14b300d12/scratchpad/hf/`.)

**Método:** leitura de código, varredura de padrões de execução arbitrária
(`eval`, `new Function`, `child_process`, `subprocess`, `shell=True`,
`postinstall`/`preinstall`), varredura de segredos por padrão
(`sk-…`, `AKIA…`, `ghp_…`, `vercel_blob_rw_…`), inventário de dependências,
inventário de hosts externos referenciados e conferência de licença.

**Limite declarado — o que NÃO é verificável nesta auditoria.** Registro aqui
porque a varredura preliminar afirmou coisas que o material local não sustenta:

- **Data de criação, número de commits e contagem de stars do repo não-oficial:
  NÃO VERIFICÁVEL.** O clone local tem **1 commit visível**
  (`b16a0ef`, 2026-09-17, `wide-trace`, "add Seedance 2 and 2.5") — é um clone
  raso. Não há como confirmar localmente "criado em 26/08/2026", "3 commits" nem
  "2.307 stars". O que **é** verificável e já basta: histórico local
  essencialmente inexistente, autoria única, zero rastro de revisão por pares.
  A tese de "star inflacionada" fica como **suspeita não comprovada**; não a uso
  como fundamento de decisão.
- **Comportamento do binário do `cli`: NÃO VERIFICÁVEL.** O repo não tem
  código-fonte Go (ver achado O-4). Não auditei o que o binário faz em runtime.
- **Retenção e destino real dos dados dentro da Higgsfield: NÃO VERIFICÁVEL por
  código.** Só se resolve por contrato (seção 3).

---

## 1. Veredito por repositório

| Repositório | Veredito | Por quê, em uma linha |
|---|---|---|
| `wide-trace/open-higgsfield` | **VETADO** | Sem licença (uso juridicamente proibido) + endpoint de upload sem autenticação + log de prompt em claro. |
| `higgsfield-ai/higgsfield-client` (Python) | **LIBERADO** | Apache-2.0 com arquivo de licença, 1 dependência, credencial por env, nenhum padrão perigoso. |
| `higgsfield-ai/higgsfield-js` | **LIBERADO COM CONDIÇÃO** | Código limpo, mas repo sem arquivo `LICENSE` apesar de declarar MIT. |
| `higgsfield-ai/skills` | **LIBERADO COM CONDIÇÃO** | MIT íntegro e scripts sãos, mas `higgsfield-soul-id` trata dado biométrico (LGPD art. 11). |
| `higgsfield-ai/cursor-plugin` | **LIBERADO COM CONDIÇÃO** | MIT, config mínima, mas aponta para MCP remoto (`mcp.higgsfield.ai`) fora do nosso controle. |
| `higgsfield-ai/homebrew-tap` | **LIBERADO** | Fórmula com `sha256` por artefato — é o caminho de instalação correto. |
| `higgsfield-ai/cli` | **LIBERADO COM CONDIÇÃO** | Binário fechado, não auditável; e `install.sh` instala com sudo sem checksum. Só via Homebrew. |

**Resumo executivo para o sócio:** a Higgsfield **não** abriu o motor de
geração. O que está no GitHub são SDKs, skills e um CLI que **chamam a API paga**
deles. O `wide-trace/open-higgsfield` **não é da Higgsfield** e não é
"open-source" — é um front-end de terceiro, sem licença, que também chama a API
paga. Adotar o stack oficial é viável sob condições; adotar o não-oficial, não.

---

## 2. Achados classificados

Severidade: **crítica** e **alta** bloqueiam. **Média** vai com prazo acordado.
**Baixa** vai para backlog.

### 2.1 `wide-trace/open-higgsfield` — candidato NÃO-oficial

| # | Risco | Sev. | Onde (prova) | Impacto | Correção | Status |
|---|---|---|---|---|---|---|
| N-1 | **Sem arquivo de licença.** O repo não tem `LICENSE`; a raiz contém apenas `README.md`, `package.json`, `src/`, `scripts/`, `public/`, configs. Mesmo assim o `README.md:1` se anuncia "Open-Source Alternative" e `README.md:18` "Free & open-source". | **Crítica** | raiz do repo (ausência de `LICENSE`); `README.md:1`, `README.md:18` | Sem licença, o padrão é "todos os direitos reservados": a KNG **não** tem direito de usar, modificar ou redistribuir. Usar em trabalho faturado é exposição jurídica direta, não teórica. | Não adotar. Só reconsiderar se o autor publicar licença OSI explícita. | **Bloqueador** |
| N-2 | **Endpoint de upload sem autenticação.** `POST /api/blob` não valida sessão, usuário nem origem; o cookie de device é apenas um rótulo de caminho, não credencial (`route.ts:16-18`, `device.ts` via `resolveDeviceId`). O próprio autor documenta a falha. | **Crítica** | `src/app/api/blob/route.ts:12` — comentário literal `// Anyone who can hit this route can upload. Gate it when auth exists.`; emissão do token em `:24-43` | Qualquer pessoa na internet que alcance a rota emite token de escrita no Vercel Blob e grava no **nosso** bucket pago (`OPEN_HIGGSFIELD_READ_WRITE_TOKEN`, `:22`). Conta de armazenamento vira conta aberta: custo ilimitado e hospedagem de conteúdo de terceiro sob domínio da KNG. O `allowedContentTypes` (`:31-39`) limita o tipo do arquivo, **não** limita quem envia nem quanto. | Exigiria autenticação real, rate limit e teto de cota antes de qualquer deploy. Não existe hoje. | **Bloqueador** |
| N-3 | **Prompt e corpo de resposta em log de servidor, em claro.** | **Alta** | `src/generation/platform.ts:55` — `console.info("[platform] request", { method, url, body: body ?? null })`; `src/generation/platform.ts:66` — `console.info("[platform] response", { …, body: payload })` | `body` é o objeto de geração montado em `to-platform.ts` — contém o **prompt integral do cliente** e as **URLs das mídias** enviadas. Esses logs caem na saída do servidor (e no provedor de hospedagem) sem redação e sem retenção definida. Se o prompt descreve campanha não lançada, ou a mídia é foto de pessoa, é vazamento de dado de cliente e tratamento de dado pessoal sem base nem prazo. | Remover os dois `console.info` ou reduzir a `{ method, url, status }`. | **Bloqueador** |
| N-4 | **Chave da plataforma guardada em texto claro no cookie.** | **Média** | `src/generation/credentials.ts:18-20` (`encodeCredentials` = `JSON.stringify({ apiKey })`), gravado em `actions.ts:22` | A chave `id:secret` viaja e repousa sem cifra. Mitigado por `httpOnly: true` (`credentials.ts:5`) e `sameSite: "lax"` (`:6`), mas `secure` só vale em produção (`credentials.ts:5`: `process.env.NODE_ENV === "production"`) — em homologação por HTTP a chave trafega em claro. Vida útil de 30 dias (`:8`). | Cifrar o valor e forçar `secure` sempre. | Ressalva (irrelevante dado o veto) |
| N-5 | **"Grátis" é marketing enganoso — é wrapper fino de API paga.** | **Média** (risco de expectativa/custo, não técnico) | `src/generation/actions.ts:70-71` (`process.env.HF_API_BASE_URL`), `actions.ts:41` (`submit`), `src/generation/platform.ts:51` + `credentials.ts:45-47` (`Authorization: Key <id:secret>`), `credentials.ts:49-54` (exige formato `id:secret`) | O app não roda modelo nenhum: repassa tudo para a API da Higgsfield com a nossa chave paga. `README.md:3-4` vende "free … 38 models"; `README.md:12` admite, em letra miúda, que exige chave própria. Quem lê o topo do README planeja custo zero e recebe fatura de API. | Tratar como cliente de API paga em qualquer análise de custo. | Ressalva |
| N-6 | **Superfície técnica limpa** (contraprova a favor do repo). | Baixa | Varredura por `eval(`, `new Function`, `child_process`, `execSync`, `postinstall`, `preinstall`: **único** resultado é `scripts/build-brand-assets.mjs:14` (`execFileSync`, script de build de assets, fora do runtime da app). 6 dependências de produção em `package.json`. Hosts externos fora do fluxo de geração: só `fonts.googleapis.com` / `fonts.gstatic.com` em `scripts/build-brand-assets.mjs:135-137`. Nenhum segredo encontrado. | Não há indício de backdoor ou exfiltração. | Nada a corrigir. | Confirmado |

**Correção do achado preliminar nº 4 — parcialmente falso.** A varredura
preliminar afirmou que **tanto** `platform.ts` **quanto** o route do blob logam
"corpo completo de request/response". Em `platform.ts` isso é verdade
(`:55`, `:66`). No route do blob **é falso**: `route.ts:19` chama
`summarizeBlobEvent(body)`, definido em `route.ts:78-83`, que emite apenas
`{ type, pathname }` ou `{ type, url }` — nunca o corpo. `route.ts:29` loga só
`{ pathname }` e `route.ts:51` loga só a **mensagem** do erro. Registro a
correção porque o veto precisa se sustentar em prova exata: o log do blob é
metadado (`pathname`/`url`), não conteúdo. O veto se apoia em N-1, N-2 e N-3.

**Decisão sobre o candidato não-oficial: VETADO.**
Bloqueadores N-1, N-2 e N-3. Não é pressão de prazo que muda isso.
**O que exatamente precisa mudar para reabrir a análise:** (a) licença OSI
publicada no repo; (b) autenticação real em `/api/blob` com rate limit e teto de
cota; (c) remoção do log de prompt e mídia em `platform.ts:55` e `:66`. Os três,
não dois.

### 2.2 Repositórios oficiais (`higgsfield-ai`)

| # | Risco | Sev. | Onde (prova) | Impacto | Correção | Status |
|---|---|---|---|---|---|---|
| O-1 | `higgsfield-js` declara `"license": "MIT"` (`package.json:48`) e lista `LICENSE` em `files` (`package.json:20`), mas **o arquivo não existe no repositório**. | **Média** | `higgsfield-js/package.json:20`, `:48`; raiz sem `LICENSE` | Metadado de licença sem texto de licença é ambíguo juridicamente. Bem mais leve que N-1 — aqui há declaração expressa de MIT pelo titular, enquanto no não-oficial não há declaração nenhuma. | Confirmar MIT com a Higgsfield por escrito **ou** usar o pacote publicado no npm, cuja tarball inclui o `LICENSE`. | Ressalva — prazo 30 dias |
| O-2 | `higgsfield-js`: credenciais só por variável de ambiente, sem fallback em disco nem telemetria. | Baixa (positivo) | `higgsfield-js/src/auth.ts:10` (`HF_CREDENTIALS`/`HF_KEY`), `:22-23` (`HF_API_KEY`/`HF_API_SECRET`), `:29` lança `CredentialsMissedError` se faltar | Comportamento correto: falha explícita em vez de seguir sem credencial. | Nada. | OK |
| O-3 | `higgsfield-js`: 2 dependências de produção (`axios`, `form-data`); varredura de `eval`/`child_process`/`postinstall` em `src/` e `package.json` retornou **nenhum**. `higgsfield-client`: 1 dependência (`httpx`, `pyproject.toml:12`), `license = "Apache-2.0"` (`pyproject.toml:8`) **com** arquivo `LICENSE` presente. | Baixa (positivo) | acima | Superfície de suprimento pequena e auditável. | Nada. | OK |
| O-4 | **`cli`: repositório sem código-fonte.** A raiz tem `LICENSE`, `README.md`, `MODELS.md`, `THIRD-PARTY-NOTICES.txt`, `demo.png`, `install.sh` — **zero** arquivo Go. O binário vem pronto das Releases (`install.sh:57`). | **Média** | raiz de `cli/`; `cli/install.sh:56-59` | "MIT" aqui cobre a documentação, não o produto. O binário que roda na máquina do time é caixa-preta: não dá para auditar o que ele lê do disco nem o que transmite. É risco aceitável para ferramenta de terceiro, **desde que** a integridade da instalação seja garantida (O-5) e o que entra nele seja controlado (seção 4). | Instalar só por caminho com verificação de integridade; tratar como software proprietário no inventário. | Ressalva — condição de adoção |
| O-5 | **`install.sh` instala binário com privilégio elevado sem verificar checksum nem assinatura.** | **Alta** | `cli/install.sh:59` (`curl -fsSL -o "$TMPDIR/$TARBALL" "$URL"`) → `:66` (`tar -xzf`) → `:78` (`run install -m 0755 "$TMPDIR/hf" "$BIN_DIR/higgsfield"`), onde `run()` (`:73-75`) escala para `sudo` se `$BIN_DIR` não for gravável. Ainda: `:79` remove a quarentena do macOS (`xattr -d com.apple.quarantine`), desligando a verificação do Gatekeeper. Entre `:49` e `:78` não existe nenhum `sha256sum`, `shasum`, `cosign` ou `gpg --verify`. | **Alta** | Um artefato adulterado (release comprometida, espelho hostil, interceptação de rede) é instalado em `/usr/local/bin` como root, sem nada que detecte a troca. É o caminho recomendado em **todas** as skills (ex.: `skills/INSTALL.md:22`, `skills/higgsfield-soul-id/SKILL.md:27`, `skills/higgsfield-brandkit/SKILL.md:28`), e as skills instruem o agente a executá-lo automaticamente — ver O-7. | **Proibir `install.sh` na KNG.** Instalar por Homebrew: `homebrew-tap/higgsfield.rb` fixa `sha256` por artefato (`:14`, `:24`, `:37`, `:46`) e versão (`:8`). | **Bloqueia o `install.sh`**, não o CLI |
| O-6 | `skills`: MIT íntegro (arquivo `LICENSE` presente, "MIT License / Copyright (c) 2026 Higgsfield AI"). 8 skills. `scripts/update-check.sh` baixa apenas o arquivo `VERSION` (`:106`), **valida com regex semver para rejeitar página de erro** (`:109`), grava em cache e no máximo **imprime** `UPGRADE_AVAILABLE` (`:121`). Não baixa binário, não executa nada, é opt-in e desativável (`:32-34`). | Baixa (positivo) | `skills/scripts/update-check.sh:106`, `:109`, `:119-121`, `:32-34` | Auto-atualização silenciosa seria risco alto. Não é o caso: confirmado que só avisa. | Nada. | OK |
| O-7 | **Skills instruem o agente a executar o instalador inseguro sozinho.** | **Média** | `skills/higgsfield-soul-id/SKILL.md:26-28`, `skills/higgsfield-brandkit/SKILL.md:28`, `skills/higgsfield-generate/SKILL.md:37`, `skills/higgsfield-websites/SKILL.md:102`, `skills/higgsfield-marketplace-cards/SKILL.md:26` ("install it by running the official installer with Bash"), `skills/INSTALL_FOR_AGENTS.md:8`, `:14` | Combinado com O-5: a skill dispara, sem pedir nada a ninguém, um `curl \| sh` que instala com sudo sem checksum. A decisão de instalação sai da mão do time. | Pré-instalar o CLI por Homebrew nas máquinas antes de habilitar as skills, para que o passo "não está no PATH" nunca dispare. Se possível, editar o passo Bootstrap na cópia interna. | Ressalva — condição de adoção |
| O-8 | `skills/higgsfield-brandkit`: chamadas de subprocesso montadas como **lista de argumentos**, nunca string de shell. | Baixa (positivo) | `higgsfield-brandkit/scripts/build_brandbook.py:508-515` (lista literal iniciada por `rsvg_convert`), `:547-552` (`subprocess.run(command, check=True, …)` com `command` sendo lista, `timeout` definido), `render_brandbook_pdf.py:30-35`. Varredura de `shell=True` e `os.system` em todo `skills/`: **nenhuma ocorrência**. | Sem injeção de comando por nome de arquivo ou nome de marca. | Nada. | OK |
| O-9 | `cursor-plugin` aponta para servidor MCP remoto da Higgsfield. | **Média** | `cursor-plugin/mcp.json:5-6` — `"url": "https://mcp.higgsfield.ai/mcp"`, tipo `http` | Um MCP remoto define do outro lado quais ferramentas o nosso agente enxerga; o conjunto pode mudar sem aviso e sem nova revisão nossa. Não há pin de versão nem trava de capacidades no arquivo. | Não habilitar por padrão. Se alguém precisar, entra como pedido nominal ao diretor de tecnologia. | Ressalva |
| O-10 | **Nenhum segredo versionado em nenhum dos sete repositórios.** | Baixa (positivo) | Varredura por `sk-…`, `AKIA…`, `ghp_…`, `vercel_blob_rw_…` nas árvores de trabalho dos 7 repos: zero ocorrências. `open-higgsfield/.env.example` traz só nomes de variáveis, valores vazios (`:1-2`). | Higiene de segredo adequada. | Ressalva de método: varri a **árvore de trabalho**, não o histórico completo (clones rasos). Varredura de histórico fica pendente para o momento da adoção. | OK, com ressalva de método |

---

## 3. LGPD — o que acontece quando prompt, imagem e rosto saem para os EUA

### 3.1 O que efetivamente sai da KNG

Confirmado no código, não presumido:

- **Prompt integral e parâmetros** — `open-higgsfield/src/generation/to-platform.ts` monta o corpo e `platform.ts:53-63` o envia à API.
- **Mídia enviada pelo cliente** — imagem de referência, foto de produto, foto de pessoa; no fluxo do repo não-oficial passa antes pelo Vercel Blob (`src/app/api/blob/route.ts`).
- **Biometria facial** — `skills/higgsfield-soul-id/SKILL.md:4-5` descreve treinar "a personalized model on a person's face"; o passo de workflow pede **"5–20 face photos, varied angles and lighting"** (`SKILL.md:42`). Isso é **dado pessoal sensível** (LGPD art. 5º, II — "dado biométrico"), e não dado pessoal comum.

Destino: infraestrutura da Higgsfield, empresa fora do Brasil (`homepage`/`repository` em `higgsfield-client/pyproject.toml:16-17`, suporte `support@higgsfield.ai`). Logo, **transferência internacional de dados** (LGPD arts. 33 a 36).

### 3.2 Base legal — por tipo de dado

| Dado | Base legal viável | Observação |
|---|---|---|
| Prompt com dado pessoal de terceiro (nome, cargo, característica de pessoa real) | Legítimo interesse (art. 7º, IX) **só** se houver expectativa razoável do titular. Em campanha, raramente há. | Regra prática: **não colocar pessoa identificável no prompt.** |
| Foto de produto, cenário, objeto, logotipo | Fora da LGPD (não é dado pessoal) — **desde que não haja pessoa enquadrada**. | É a faixa segura do stack. |
| Foto com rosto de pessoa (cliente, funcionário, modelo) | **Consentimento específico e destacado** (art. 7º, I + art. 9º). Contrato de prestação de serviço **não** cobre. | Precisa de autorização de uso de imagem que mencione geração por IA e transferência ao exterior. |
| Treino de Soul / identidade facial | **Consentimento específico para dado sensível** (art. 11, I). Nada mais serve. | O mais arriscado do stack inteiro. |

**Papéis:** o cliente da KNG é o **controlador** do dado do próprio público; a KNG
é **operadora**; a Higgsfield é **suboperadora**. A KNG responde solidariamente
(art. 42, §1º, II) pelo que manda para lá.

### 3.3 Retenção

**Não verificável por código.** Nenhum dos sete repositórios expõe política de
retenção, prazo de expurgo ou endpoint de exclusão. `platform.ts:76-79` só
consulta status por `request_id`; não há `DELETE`. O que se sabe é que os
resultados voltam como **URLs** (`platform.ts:98-110`), o que indica que a mídia
**permanece hospedada do lado deles** por prazo que não controlamos nem
conhecemos. Presumir "eles apagam depois" é presunção, não achado. Só contrato
resolve.

### 3.4 O que a KNG precisa ter ANTES de mandar material de cliente

Condições cumulativas. Sem as seis, não sai material de cliente.

1. **Contrato de operador / DPA assinado com a Higgsfield**, com: finalidade limitada, proibição de uso do nosso material para treinar modelos deles, prazo de retenção expresso, rotina de exclusão sob demanda e obrigação de notificar incidente.
2. **Cláusula de transferência internacional** (arts. 33-35), com garantias adequadas e menção ao país de destino.
3. **Aditivo no contrato da KNG com cada cliente** informando que a produção usa IA generativa de terceiro sediado no exterior, e **autorização escrita** para enviar o material dele.
4. **Autorização de uso de imagem** específica para cada pessoa retratada, mencionando geração por IA e transferência ao exterior — obrigatória, e com consentimento de dado sensível (art. 11) quando houver treino de identidade facial.
5. **Registro de operações de tratamento** (art. 37): o que foi enviado, de qual cliente, quando, com qual finalidade, sob qual base legal.
6. **Encarregado (DPO) nomeado** e plano de resposta a incidente com prazo e responsável definidos, cobrindo explicitamente o cenário "vazamento no fornecedor de IA".

**Enquanto 1 a 4 não existirem:** o stack só pode ser usado com material da
**própria KNG** (marca da agência, peça de portfólio interna, teste), nunca com
material de cliente e nunca com rosto de pessoa.

---

## 4. Condições operacionais obrigatórias se o stack oficial for adotado

**Guarda de chave**
- Chave `id:secret` só em cofre de segredos e injetada como variável de ambiente (`HF_CREDENTIALS`/`HF_KEY`, conforme `higgsfield-js/src/auth.ts:10`). Nunca em planilha, chat, e-mail, `.env` versionado ou comentário de código.
- Uma chave por ambiente (produção / experimentação) e uma por pessoa quando a plataforma permitir, para dar rastro e revogação individual.
- Rotação a cada 90 dias e **revogação imediata** na saída de qualquer colaborador.
- 2FA obrigatório na conta Higgsfield e no cofre.

**Instalação**
- **CLI: só por Homebrew** (`brew install higgsfield-ai/tap/higgsfield`), que verifica `sha256` (`homebrew-tap/higgsfield.rb:14`, `:24`, `:37`, `:46`).
- **`cli/install.sh` proibido** na KNG — achado O-5 (sudo sem checksum, `:74`/`:78`, e remoção de quarentena, `:79`).
- SDKs a partir dos registries oficiais (npm `@higgsfield/client`, PyPI `higgsfield-client`), com lockfile versionado.
- Pré-instalar o CLI **antes** de habilitar as skills, para neutralizar o passo Bootstrap que dispara o instalador (O-7).

**Atualização**
- Versão fixada (pin) e atualização revisada por pessoa. Nada de auto-update.
- `skills/scripts/update-check.sh` pode ficar ligado: só avisa (O-6). Se preferirem silêncio, basta criar `~/.higgsfield-skills/update-check-disabled` (`update-check.sh:32-34`).
- Rodar `npm audit` / auditoria de dependências a cada atualização; nenhum crítico em aberto.
- Reauditar este parecer a cada mudança maior de versão do CLI ou das skills.

**O que NUNCA pode ir para a API**
- Rosto ou voz de pessoa identificável sem autorização escrita específica (item 4 da seção 3.4).
- Qualquer treino de identidade facial (`higgsfield-soul-id`) sem consentimento de **dado sensível** documentado.
- Documento de identificação, dado de saúde, dado de criança ou adolescente — em nenhuma hipótese.
- Material sob NDA, campanha não lançada, preço não divulgado, informação estratégica de cliente.
- Credencial, token, print de painel administrativo ou qualquer captura de tela com dado de produção.
- Base de dados de cliente, lista de contatos, planilha de lead.

**Controles de processo**
- `cursor-plugin` / MCP remoto (`mcp.json:5-6`) **desabilitado por padrão**; habilitação nominal e justificada.
- Log de uso interno: quem gerou, para qual cliente, com qual finalidade.
- Saída de IA generativa nunca vai ao cliente sem passar pelo `agente-revisor-marca` e, quando houver pessoa, promessa ou setor regulado, pelo gatilho jurídico.

---

## 5. Consolidado da decisão

**Decisão:** `liberado_com_ressalvas` para o stack **oficial** · **VETADO** para o candidato **não-oficial**.

**Bloqueadores (impedem adoção):**
1. `wide-trace/open-higgsfield` — ausência de licença (N-1, crítico).
2. `wide-trace/open-higgsfield` — upload sem autenticação (N-2, crítico), `src/app/api/blob/route.ts:12`.
3. `wide-trace/open-higgsfield` — log de prompt e mídia em claro (N-3, alto), `src/generation/platform.ts:55` e `:66`.
4. `cli/install.sh` como método de instalação (O-5, alto) — **proibido**; o CLI em si segue liberado por Homebrew.

**Ressalvas (vão com prazo definido):**
- O-1 — confirmar MIT do `higgsfield-js` por escrito ou consumir do npm. **30 dias.**
- O-4 — registrar o CLI como software proprietário no inventário, com dono responsável. **30 dias.**
- O-7 — pré-instalar o CLI por Homebrew antes de liberar as skills. **Antes do primeiro uso.**
- O-9 — MCP remoto desabilitado por padrão; habilitação nominal. **Imediato.**
- Seção 3.4, itens 1 a 4 — enquanto não existirem, uso restrito a material da própria KNG. **Trava a entrada de material de cliente.**
- O-10 — varredura de segredos no histórico completo (clones atuais são rasos). **No ato da adoção.**

**Recomendações de longo prazo:**
- Camada interna própria entre a KNG e a API, para centralizar chave, aplicar rate limit, redigir log e manter o registro de tratamento do art. 37 — em vez de espalhar a chave por máquinas de pessoas.
- Avaliar motor auto-hospedado para o que envolver rosto de pessoa; é o único caminho que elimina a transferência internacional em vez de contratualizá-la.
- Rever o parecer a cada 6 meses ou a cada mudança maior de versão.

---

## Ficha de Aprovação

| Campo | Valor |
|---|---|
| Entregável | `KNG-INT-SEG-01` — Parecer de Segurança — Motor de Geração (stack Higgsfield) |
| Executor | `agente-seguranca` |
| Cadeia | `agente-seguranca` → `diretor-de-tecnologia` |
| Rodada | 1 de 2 |

### Passagem pela cadeia
Cada aprovador preenche **só a sua linha**, na ordem.

| # | Aprovador | Decisão | Data | Parecer detalhado em |
|---|-----------|---------|------|----------------------|
| 1 | `diretor-de-tecnologia` | ☐ aprovado ☐ ajustes | | (este arquivo é o parecer) |

**Gatilho jurídico:** ☐ não se aplica ☐ acionado — laudo em `<caminho>`
(promessa, comparação, pessoa nomeada, preço, alegação de composição ou setor
regulado. Laudo `RISCO ALTO` bloqueia, mesmo com a cadeia toda aprovando.)

**Decisão final (quem fecha a cadeia):**
☐ aprovado_interno ☐ ajustes_solicitados ☐ bloqueado

**Ajustes obrigatórios:**
1.
2.
3.

**Pendências que travam a PUBLICAÇÃO mas não a aprovação interna:**
- `[CONFIRMAR COM ...]` em aberto

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
