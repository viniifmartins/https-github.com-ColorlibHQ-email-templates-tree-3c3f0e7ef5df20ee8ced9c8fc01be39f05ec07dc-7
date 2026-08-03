# Como contratar um novo funcionário (adicionar um agente)

## 1. Antes de criar, pergunte

- Esse trabalho já não é de alguém do time? (evite agente que se sobrepõe)
- Ele produz um **entregável próprio**? Se não produz arquivo, provavelmente é
  uma instrução dentro de um agente existente, não um agente novo.
- Quem aprova o que ele faz? Se a resposta for "ele mesmo", pare — não vale.

## 2. Crie `.claude/agents/<nome>.md`

```yaml
---
name: agente-xxx                 # igual ao nome do arquivo, minúsculo, com hífen
description: <quando acionar>    # é por aqui que o gerente decide delegar. Seja específico.
tools: Read, Write, Edit, Glob, Grep
model: opus | sonnet
departamento: <um dos de time.json>
cargo: <cargo humano>
reporta_para: <agente>
aprovado_por: <agente>           # nunca ele mesmo
recebe_de: <agente>
entrega_para: <agente>
---
```

Corpo do arquivo, sempre nesta ordem:

1. **Quem você é** — uma frase que define o padrão de qualidade.
2. **Entradas obrigatórias** — arquivos e status exigidos. Com a ordem de parar
   se faltar algo.
3. **Processo** — passo a passo, numerado.
4. **Formato de saída** — o arquivo gerado, com estrutura literal.
5. **Regras** — o que separa bom de medíocre nessa função.
6. **Nunca** — 3 a 5 proibições duras.

## 3. Registre em `equipe/time.json`

Adicione o objeto do funcionário (departamento, aprovações, avatar, mesa).
Rode `python3 -c "import json;json.load(open('equipe/time.json'))"` para validar.

## 4. Atualize o roteamento

Inclua a linha correspondente na tabela "quem aciono agora?" do
`.claude/agents/gerente-de-contas.md` e no organograma de `docs/00-visao-geral.md`.

## 5. Rode os dois validadores

```bash
python3 scripts/validar_time.py          # estrutura do time
python3 scripts/validar_entregaveis.py   # entregáveis dos clientes
```

Zero erro antes de commitar.

## Pegadinha: agente novo só aparece depois de reabrir a sessão

O Claude Code carrega a lista de subagentes no início da sessão. Se você criar um
`.claude/agents/*.md` no meio de uma conversa, ele ainda não pode ser acionado
como subagente ali — **feche e reabra a sessão**. Enquanto isso, os validadores
já conseguem checá-lo normalmente, porque leem o arquivo direto do disco.

## Boas práticas de prompt aprendidas aqui

- **Descrição vale mais que corpo.** O `description` é o que faz o agente ser
  escolhido. "Use quando X, depois de Y, antes de Z" funciona muito melhor que
  "especialista em X".
- **Proíba explicitamente.** A seção "Nunca" evita mais retrabalho que qualquer
  instrução positiva.
- **Peça formato literal.** Blocos de exemplo produzem saída consistente;
  descrição abstrata produz variação.
- **Exija citação.** "Cite o trecho do DNA que foi violado" força verificação
  real em vez de opinião.
- **Um agente, um entregável.** Agente que faz três coisas faz as três mal.
- **O gate precisa estar na seção de entradas, não só nas regras.** Nos testes, o
  que fez o `agente-dna-marca` recusar trabalhar sob pressão de prazo foi a linha
  "Sem isso, pare" logo na primeira seção — não a proibição lá no fim.
