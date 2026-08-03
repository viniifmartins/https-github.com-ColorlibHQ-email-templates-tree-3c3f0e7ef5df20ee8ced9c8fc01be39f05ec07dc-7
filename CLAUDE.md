# Agência KNG — Regras Globais

Este repositório é o "escritório" da KNG. Cada agente em `.claude/agents/` é um
funcionário com uma função específica. Nenhum agente trabalha sozinho: todo
entregável passa por um aprovador antes de seguir para a próxima etapa.

## Princípios inegociáveis

1. **Ninguém pula fila.** Um agente só começa quando os insumos de que depende
   estão com `status: aprovado_interno` (ou `aprovado_cliente`, quando o gate exigir).
2. **Tudo vira arquivo.** Nenhuma entrega existe só no chat. Toda saída é um `.md`
   dentro de `clientes/<cliente>/<fase>/`, no formato do
   [Protocolo de Handoff](docs/02-protocolo-de-handoff.md).
3. **O DNA da marca é a lei.** Qualquer peça que contrarie
   `clientes/<cliente>/01-marca/dna-marca.md` é reprovada pelo `agente-revisor-marca`.
4. **Quem aprova não é quem executa.** O aprovador de cada agente está declarado
   no frontmatter (`aprovado_por`). Auto-aprovação é proibida.
5. **O cliente fala com uma pessoa só.** Todo contato externo passa pelo
   `gerente-de-contas`. Agentes de execução nunca falam direto com o cliente.
6. **Reprovar é barato, retrabalho é caro.** Ao reprovar, o aprovador escreve
   o motivo e o que exatamente precisa mudar — nunca "não gostei".

## Idioma e tom

Todo entregável é em **pt-BR**. Documentos internos podem ser diretos e técnicos.
Documentos que vão ao cliente seguem o tom definido no DNA da marca do cliente.

## Estrutura de pastas de um cliente

```
clientes/<cliente>/
├── 00-descoberta/   perguntas iniciais, respostas, briefing
├── 01-marca/        dna-marca, logo, identidade visual
├── 02-projeto/      escopo, cronograma, orçamento
├── 03-criacao/      copy, imagens, posts
├── 04-web/          arquitetura, seo, dev, performance, segurança
├── 05-conteudo/     calendário editorial, entregas recorrentes
├── 06-midia/        analytics, tráfego pago, resultado
├── relatorios/      o que foi enviado ao cliente, por data
└── status.md        painel do gerente de contas
```

## Antes de commitar qualquer mudança no time

```bash
python3 scripts/validar_time.py
```

Zero erro é obrigatório. O validador pega auto-aprovação, aprovador inexistente,
ciclo de chefia, divergência entre os `.md` e o `equipe/time.json` e link quebrado
na documentação.

## Como o time é acionado

O ponto de entrada é sempre o `gerente-de-contas`. Ele lê o estado da pasta do
cliente, decide qual é a próxima etapa e delega. Se você (humano) quiser acionar
um especialista direto, tudo bem — mas o gerente ainda precisa registrar o
resultado no fluxo.
