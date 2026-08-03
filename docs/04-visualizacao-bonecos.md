# Fase 2 — Ver os funcionários trabalhando (modo "bonecos")

Esta estrutura já foi desenhada para virar visualização. Nada precisa ser
refeito: o `equipe/time.json` é a planta do escritório e os arquivos de
entregável são o que dá vida ao boneco.

## De onde vem cada coisa

| Na tela | Vem de |
|---------|--------|
| Personagem (avatar, cor, acessório) | `equipe/time.json` → `funcionarios[].avatar` |
| Sala / posição da mesa | `avatar.mesa` `[coluna, linha]` + `departamentos[].sala` |
| Linhas de hierarquia | `reporta_para` |
| Setas de fluxo de trabalho | `recebe_de` / `entrega_para` |
| Carimbo de aprovação | `aprova` / `aprovado_por` |
| Estado atual do boneco | `status` no frontmatter dos entregáveis do cliente |
| Balão de fala | linha `DECISÕES:` da devolutiva do agente |
| Balão de alerta | `bloqueado`, `ajustes_solicitados`, veto de segurança |

## Estados e a animação correspondente

| status do entregável | boneco |
|---|---|
| não existe | mesa vazia, funcionário `ocioso` |
| `rascunho` | digitando |
| `em_revisao` | papel voando da mesa dele para a mesa do aprovador |
| `ajustes_solicitados` | papel voltando + balão vermelho |
| `aprovado_interno` | carimbo verde |
| `aprovado_cliente` | confete / troféu na mesa do gerente |

## Como gerar o estado em tempo real

Um script simples varre `clientes/<cliente>/**/*.md`, lê o frontmatter
(`autor`, `aprovador`, `status`, `versao`) e emite um `estado.json`:

```json
{
  "cliente": "padaria-do-ze",
  "atualizado_em": "2026-08-03T14:02:00Z",
  "funcionarios": {
    "agente-logo": { "estado": "em_revisao", "entregavel": "KNG-PADARIA-MARCA-01", "com": "agente-revisor-marca" },
    "agente-seo":  { "estado": "aguardando_insumo", "esperando": "KNG-PADARIA-WEB-01" }
  }
}
```

A visualização (HTML + canvas/SVG, ou pixel art estilo escritório) consome
`time.json` (layout fixo) + `estado.json` (o que muda). Enquanto o script não
existe, o `gerente-de-contas` já mantém o mesmo dado em `status.md`.

## Sugestão de próximos passos

1. Rodar 1 cliente real de ponta a ponta com o time atual.
2. Escrever o script `estado.json` (30 a 50 linhas de Python).
3. Só então construir a tela. Visualização de um fluxo que ainda não foi
   validado na prática vira retrabalho.
