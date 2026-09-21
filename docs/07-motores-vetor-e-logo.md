# Motor vetor e motor gerador de logo — pesquisa e especificação

Documento de pesquisa e desenho técnico dos dois motores que faltam na base,
identificados em [06-revisao-da-base.md](06-revisao-da-base.md) (itens 14 e 15).
Pesquisa feita em 21/09/2026; fontes no fim do arquivo, todas com URL.

Nada aqui está implementado ainda. Este arquivo existe para que a implementação
não comece por chute e para que a decisão de ferramenta seja auditável depois.

---

## Parte 1 — Motor vetor (vetorial perfeito)

### O problema real

"Vetorizar" e "vetor perfeito" são coisas diferentes, e quase todo produto de
mercado entrega a primeira fingindo que é a segunda.

- **Traçar** é aproximar pixels por curvas. Sai um SVG que *parece* o bitmap,
  com centenas de nós, curvas quase-simétricas, raios quase-iguais e ângulos
  quase-retos.
- **Vetor perfeito**, para logo, é outra coisa: a forma é **reconstruída** com
  intenção geométrica — simetria exata, tangência real, raios idênticos,
  alinhamento a grid, o mínimo de nós que descreve a forma.

Um logo com 380 nós e simetria aproximada funciona na tela e falha em tudo o
que importa: corte de vinil, bordado, gravação, fachada, favicon de 16px e
qualquer redesenho futuro. Nenhum traçador resolve isso sozinho — o que falta
no mercado, e é onde a KNG pode ser melhor, é o **estágio de regularização**
entre o traçado e a entrega.

### Arquitetura proposta — 5 estágios

```
E0 entrada        E1 traçado         E2 regularização    E3 limpeza      E4 validação     E5 empacotamento
bitmap de estudo  VTracer/Potrace    simetria, raios,    SVGO, nós       gates            variantes,
SVG gerado por IA  → SVG bruto       tangência, grid     redundantes,    automáticos      formatos,
arquivo do cliente                   primitivas          1 path/forma    (reprova)        manifesto
```

#### E0 — Entrada

Três origens possíveis, e o motor precisa saber qual é:
bitmap de estudo (IA ou rascunho), SVG gerado (text-to-SVG), ou **arquivo do
cliente** — este último é o caso da trilha C, e é onde o motor vale mais: pegar
o JPG de 900px que a empresa usa há oito anos e devolver o vetor que ela nunca
teve.

#### E1 — Traçado

| Ferramenta | Quando usar | Por quê |
|---|---|---|
| **VTracer** (Rust, open source) | entrada colorida, foto, logo com mais de uma cor | pipeline **O(n)** contra **O(n²)** do Potrace; aceita cor direto; o modo hierárquico empilha formas em vez de recortá-las, o que gera SVG mais compacto e sem furos que o Image Trace do Illustrator |
| **Potrace** (via Inkscape CLI) | arte preto-e-branco de alto contraste | resultado mais suave em binário, cadeia estável e previsível, saída também em PDF/EPS/DXF |

Regra: entrada binária limpa → Potrace; qualquer outra coisa → VTracer. Ambos
são locais, sem upload em nuvem, o que também resolve confidencialidade de
marca não lançada.

#### E2 — Regularização geométrica (o estágio que ninguém faz)

É aqui que "vetorial perfeito" acontece. Sobre o SVG bruto do E1:

1. **Detectar intenção** — casar trechos contra primitivas (círculo, arco,
   retângulo, polígono regular, linha) dentro de uma tolerância declarada.
2. **Forçar o que era aproximado** — simetria (eixo vertical/horizontal/radial),
   raios iguais, centros concêntricos, ângulos em múltiplos escolhidos,
   espessura de traço constante.
3. **Continuidade** — garantir G1 (tangente) e, onde a forma pede, G2
   (curvatura) nas junções; remover micro-nós que quebram a curva.
4. **Grid** — encaixar o resultado no grid de construção que o `agente-logo`
   definiu (proporção, área de respiro, tamanho mínimo). O grid deixa de ser
   ilustração do manual e vira restrição executável.

Ferramentas: **svgpathtools** (Python — classes `Line`, `QuadraticBezier`,
`CubicBezier`, `Arc`, cálculo de tangente, normal, curvatura e interseção
eficiente entre paths) para medir e reconstruir; **PathBool.js** ou **paper.js**
para operações booleanas; expansão de traço para contorno antes de qualquer
booleana.

#### E3 — Limpeza e normalização

**SVGO**, mais um passe próprio que o SVGO não faz: `viewBox` normalizado, um
path por forma, sem `transform` aninhado, sem `stroke` não expandido, sem
gradiente, sem filtro, `currentColor` onde a cor é semântica, IDs previsíveis,
precisão decimal fixa (3 casas resolve qualquer aplicação física).

#### E4 — Validação automática (gate, não relatório)

Hoje a base tem gate para texto (copydesk), para DNA (revisor-marca) e para
técnica (diretor-de-tecnologia). Para **arquivo de marca** não existe nenhum.
Este é o gate; reprova sozinho, antes de qualquer humano olhar:

- [ ] contagem de nós dentro do teto declarado para a rota
- [ ] contagem de cores ≤ o que o `identidade-visual` autorizou
- [ ] legível a 16px (render + diff perceptual contra o render a 512px)
- [ ] versão monocromática não fecha contraforma nem vira mancha
- [ ] versão em negativo funciona
- [ ] simetria declarada é simetria real (tolerância em unidades, não "parece")
- [ ] sem `stroke` vivo, sem gradiente, sem filtro, sem texto não convertido
- [ ] peso final e nº de paths dentro do orçamento
- [ ] abre igual em navegador, Figma e Illustrator (render comparado)
- [ ] diff perceptual contra o estudo aprovado acima do limiar — se a
      regularização mudou a forma além do combinado, **volta**, não passa

#### E5 — Empacotamento

Variantes que o `agente-logo` já exige (principal, horizontal, reduzida,
monocromática, negativa) × formatos: SVG otimizado, PNG em N tamanhos, favicon,
PDF/EPS via Inkscape CLI, e logotipo em fonte quando o caso justificar. Tudo
sai com o **manifesto** do item 17 da revisão (id, status, arquivos, hash),
para continuar dentro do protocolo de handoff.

### O que a pesquisa acadêmica recente resolve — e o que não resolve

Há trabalho novo e forte em vetorização por aprendizado: **AnchorFlow**
(reconstrução editável via campos esparsos de pontos de ancoragem),
**VectorArk** (representação por polígono arredondado), **SuperSVG** (síntese
baseada em superpixel). Todos miram **ilustração e fotografia**: fidelidade
visual com número controlado de primitivas.

Para **logo**, isso não é o objetivo. Logo precisa de exatidão geométrica e
mínimo de nós, não de fidelidade fotográfica. A conclusão prática da pesquisa:
**traçado clássico (E1) + regularização própria (E2) é o caminho certo para
marca**; os modelos aprendidos entram, no máximo, como alternativa de E1 para
material ilustrativo do `agente-imagens`.

---

## Parte 2 — Motor gerador de logo

O `agente-logo` atual já faz a parte estratégica bem: diagnóstico de clichê de
categoria, 3 rotas realmente diferentes, recomendação com opinião, briefing de
execução, prompts. O que falta é **gerar** — e gerar de um jeito que não
dependa de sorte de prompt.

### Camada 1 — Insumo (não é opcional)

Pesquisa completa (`00-descoberta/pesquisa-mercado.md` +
`00-descoberta/demanda-busca.md`, itens 5 e 6 da revisão) + DNA aprovado +
matriz de forma da categoria: o que a categoria inteira já usa (e que portanto
está proibido) contra o espaço visual livre. Sem essa matriz, "distintivo" é
opinião.

### Camada 2 — Geração por três vias, em paralelo

| Via | Como | Resultado |
|---|---|---|
| **A. Tipográfica/monograma paramétrica** | construção por código a partir de fonte licenciada: ajuste de contraforma, tracking ótico, corte e fusão de hastes | determinística, já nasce vetor limpo, zero risco de "IA inventou letra" |
| **B. Geométrica paramétrica** | código: grid, razões, malha, booleanas, variação por *seed* | dezenas de variações reprodutíveis; o mesmo seed devolve a mesma forma, sempre |
| **C. IA como estudo** | raster (exploração de forma) + text-to-SVG | amplitude e surpresa; **nunca** arquivo final |

Modelos pesquisados para a via C:

- **OmniSVG** (NeurIPS 2025, StepFun + Fudan) — primeira família end-to-end de
  geradores de SVG sobre VLMs pré-treinados, com Text-to-SVG, Image-to-SVG e
  Character-Reference; supera as linhas de base em seguir instrução e em
  qualidade estética. Tem também **OmniLottie** (mar/2026) para animação — o que
  conecta direto com o `agente-video`.
- **StarVector** (8B) — LLM com encoder de imagem para Image-to-SVG; falha em
  SVG complexo, então serve para ícone e forma simples, que é exatamente o caso
  de logo.
- **Chat2SVG** — LLM + difusão para gerar template semântico; precisa de
  otimização posterior do script SVG, o que pesa no tempo de execução.

Decisão que sai daí: usar text-to-SVG como **fonte de estudo estrutural**, não
como saída. Todo resultado da via C entra obrigatoriamente no motor vetor (E0)
e só existe como entregável depois do E4.

### Camada 3 — Filtro automático antes do olho humano

Apresentar 40 opções ao diretor é transferir trabalho, não entregar trabalho.
Antes de qualquer humano, o motor descarta o que já dá para descartar por
medida: colisão com a matriz de clichê, falha de legibilidade a 16px, falha em
monocromático, excesso de nós, proximidade excessiva com marca existente
encontrada na pesquisa. O que sobra vai para `revisor-marca` →
`diretor-de-criacao`, na cadeia que já existe.

### Camada 4 — Saída

Rota recomendada em vetor final (E5) + variantes + tokens do
`identidade-visual` + prova de uso em aplicação real. E o **registro de
proveniência** que hoje só as imagens têm: via usada, modelo, versão, seed,
prompt, data, direitos — item 16 da revisão.

### Gate jurídico, antes do cliente ver

Marca gerada com apoio de IA tem dois riscos que o fluxo atual não cobre:
registrabilidade e semelhança com marca já registrada. A checagem de colisão no
**INPI** precisa acontecer **antes** da apresentação — existe API de terceiros
para automatizar a consulta à base oficial (`busca.inpi.gov.br`), com opções de
consulta individual e em lote. O `agente-juridico` já tem `WebSearch` e já tem
poder de veto: falta só a etapa estar declarada na cadeia.

---

## Parte 3 — Stack de apoio pesquisada

### Pesquisa e SEO avançado (itens 5 e 6)

| Fonte | Uso | Observação |
|---|---|---|
| **DataForSEO** | SERP e métricas de palavra-chave via API | ~US$ 0,0006/consulta na fila normal, ~US$ 0,002 no *live*; é infraestrutura pura, sem interface — feito para automação |
| **Semrush API** | base de keyword, anúncios, tráfego | mais abrangente, caro; só faz sentido se já houver assinatura |
| **SE Ranking / SerpApi** | alternativas intermediárias | melhor relação custo/uso para volume médio |
| **Google Search Console API** | dado real do próprio cliente | insubstituível para site existente; não serve para cliente novo |
| **INPI (via API de terceiros)** | colisão de marca | consulta individual ou em lote sobre a base oficial |

Enquanto não houver contrato de API, o fallback é `WebSearch`/`WebFetch` com
protocolo de amostragem declarado — mas **com a limitação escrita no
entregável**: "volume estimado, sem fonte de dados contratada" é honesto;
número inventado com cara de precisão, não.

### Design system (itens 9, 10, 11, 12)

- **DTCG / Design Tokens Format Module 2025.10** — primeira versão estável
  (out/2025), estrutura com `$value` e `$type` e referência entre tokens por
  caminho; módulos Format, Color e Resolver. Lido/escrito por Figma, Penpot,
  Sketch, Tokens Studio, Style Dictionary e Terrazzo. É o formato de entrega.
- **Style Dictionary / Terrazzo** — build dos tokens para CSS, Tailwind, iOS,
  Android.
- **Contraste** — WCAG 2 (AA) como piso obrigatório; **APCA** como leitura de
  legibilidade (Lc, sensível a tamanho e peso da fonte). O contraste saiu do
  rascunho do WCAG 3 em 2023 e, em abr/2026, o algoritmo do WCAG 3 continua "a
  definir" — então APCA **informa**, WCAG 2 **reprova**.
- **Shaders** — `paper-design/shaders`: 30+ efeitos WebGL (mesh gradient, grain,
  liquid metal, god rays), **Apache-2.0**, uso comercial livre e sem
  atribuição, zero dependências, pacotes `@paper-design/shaders` e
  `@paper-design/shaders-react`. É o caminho de menor custo para a camada
  generativa da marca. Requisitos que a KNG precisa impor por cima:
  fallback estático, `prefers-reduced-motion`, orçamento de GPU/bateria e
  medição no `agente-performance`.

---

## Fontes

Vetorização e SVG
- [VTracer — visioncortex/vtracer](https://github.com/visioncortex/vtracer)
- [VTracer: The Revolutionary Raster-to-Vector Graphics Converter](https://www.blog.brightcoding.dev/2026/03/25/vtracer-the-revolutionary-raster-to-vector-graphics-converter)
- [Comparison of raster-to-vector conversion software — Wikipedia](https://en.wikipedia.org/wiki/Comparison_of_raster-to-vector_conversion_software)
- [image2svg-awesome](https://github.com/fromtheexchange/image2svg-awesome)
- [svgpathtools](https://github.com/mathandy/svgpathtools)
- [PathBool.js](https://github.com/r-flash/PathBool.js)
- [AnchorFlow: Editable SVG Reconstruction via Sparse Anchor Point Fields](https://arxiv.org/pdf/2605.19551)
- [VectorArk: Learning Practical Image Vectorization with Rounded Polygon Representation](https://arxiv.org/pdf/2605.24398)
- [SuperSVG: Superpixel-based Scalable Vector Graphics Synthesis](https://arxiv.org/pdf/2406.09794)

Geração de logo e SVG por IA
- [OmniSVG: A Unified Scalable Vector Graphics Generation Model (NeurIPS 2025)](https://arxiv.org/html/2504.06263v1)
- [OmniSVG — repositório](https://github.com/OmniSVG/OmniSVG)
- [OmniSVG — página do projeto](https://omnisvg.github.io/)
- [Chat2SVG: Vector Graphics Generation with LLMs and Image Diffusion Models](https://www.researchgate.net/publication/394643692_Chat2SVG_Vector_Graphics_Generation_with_Large_Language_Models_and_Image_Diffusion_Models)

Design system, tokens e contraste
- [Design Tokens specification reaches first stable version — W3C DTCG](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/)
- [Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/)
- [WCAG3 Contrast as of April 2026 — Adrian Roselli](https://adrianroselli.com/2026/04/wcag3-contrast-as-of-april-2026.html)
- [APCA in a Nutshell](https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.html)
- [paper-design/shaders](https://github.com/paper-design/shaders)

Pesquisa, SEO e registro de marca
- [DataForSEO API: Complete 2026 Guide (Pricing + Endpoints)](https://nextgrowth.ai/dataforseo-api-guide/)
- [7 Best Semrush API Alternatives for SEO Data in 2026](https://seranking.com/blog/semrush-api-alternatives/)
- [INPI — busca de marcas (base oficial)](https://busca.inpi.gov.br/pePI/servlet/LoginController?action=login)
- [API de consulta INPI / Marcas — Infosimples](https://infosimples.com/consultas/inpi-marcas/)

Diagnóstico de marca existente (trilhas A/B/C)
- [Brand Audit Framework: How to Evaluate Your Brand in 2026](https://www.atla.design/journal/brand-audit-framework)
- [Brand Refresh vs. Rebrand: A Strategic Guide](https://www.biteblueprint.com/refresh-vs-rebrand-a-guide-for-marketing-managers-to-evolve-their-visual-identity/)
