# Protocolo de Handoff

Todo entregável é um arquivo `.md` que **começa** com este frontmatter:

```yaml
---
id: KNG-<CLIENTE>-<FASE>-<NN>      # ex: KNG-PADARIA-MARCA-01
cliente: padaria-do-ze
fase: 01-marca
titulo: Manual de Identidade Visual
autor: agente-identidade-visual
aprovador: diretor-de-criacao
status: em_revisao
versao: v1
data: 2026-08-03
depende_de: [KNG-PADARIA-DESC-02, KNG-PADARIA-MARCA-01]
---
```

## Regras de leitura (o que um agente faz ao ser acionado)

1. Ler `CLAUDE.md` e o próprio arquivo de agente.
2. Listar `clientes/<cliente>/` e ler **todos** os arquivos citados nas suas
   "Entradas obrigatórias".
3. Verificar o `status` de cada entrada. Se alguma não estiver aprovada, **parar**
   e devolver ao `gerente-de-contas` dizendo exatamente o que está faltando.
4. Só então produzir.

## Regras de escrita

- Um entregável = um arquivo. Nada de arquivo gigante com tudo dentro.
- Nunca sobrescrever uma versão aprovada. Nova versão = `v2` no frontmatter e
  changelog no fim do arquivo.
- Nunca editar arquivo de outro agente. Se precisa de mudança, abre um pedido no
  entregável do gerente.
- Sempre terminar com a Ficha de Aprovação em branco (o aprovador preenche).

## Devolutiva padrão ao gerente

Ao terminar, o agente responde ao `gerente-de-contas` com, no máximo, 8 linhas:

```
ENTREGA: <id> — <titulo>
ARQUIVO: <caminho>
STATUS: em_revisao
DECISÕES: <2-3 escolhas relevantes que fiz>
PENDÊNCIAS: <o que ficou faltando e de quem depende>
PRÓXIMO: <quem deve ser acionado agora>
```
