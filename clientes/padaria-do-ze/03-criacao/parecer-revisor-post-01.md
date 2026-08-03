---
id: KNG-PADARIA-REV-01
cliente: padaria-do-ze
fase: 03-criacao
titulo: Parecer — Revisor de Marca sobre Post 01 (Encomendas de Natal)
autor: agente-revisor-marca
aprovador: diretor-de-criacao
status: ajustes_solicitados
versao: v1
data: 2026-08-03
depende_de: [KNG-PADARIA-MARCA-00, KNG-PADARIA-CRIA-01]
---

## Alerta prévio de processo (bloqueante, anterior ao mérito)

O `dna-marca.md` (KNG-PADARIA-MARCA-00) está com `status: em_revisao` no
frontmatter e sua Ficha de Aprovação está em branco:

> **Decisão:** ( ) aprovado_interno  ( ) aprovado_cliente  ( ) reprovado

Ou seja: não há DNA `aprovado_cliente`. Por regra de agência, nenhuma peça de
criação deveria ter sido produzida a partir de um DNA nesse estado, e este
revisor não pode dar `aprovado_interno` a peça alguma enquanto isso não for
regularizado — independentemente do mérito do texto. Isso já bastaria para
barrar o post. Ainda assim, a análise de conteúdo abaixo segue, porque o post
viola o DNA de forma tão extensa que o retrabalho precisa ser total de
qualquer forma.

## Parecer — Revisor de Marca

**Decisão:** ajustes_solicitados

| Critério | Nota | Observação |
|---|---|---|
| Propósito | 1 | O post vende a tese oposta ao propósito da marca ("linha gourmet premium" em vez de "pão de verdade não precisa virar artigo de luxo"). |
| Posicionamento | 1 | O texto se posiciona como concorrente de luxo/gourmet — exatamente o território que o DNA reserva à Trigo Dourado, que é quem a marca existe para contestar. |
| Tom de voz | 1 | "Prezado cliente" é o exemplo literal de personalidade proibida; não há segunda pessoa de balcão, é discurso corporativo genérico. |
| Público | 2 | Fala com "consumidor a converter" (urgência, CTA de funil), não com o vizinho/Seu Antônio/Juliana definidos como persona. |
| Consistência visual | 3 | O post não descreve nenhuma imagem real do forno/produto/preço (Território Visual exige prova fotográfica); por ser peça só de copy, não há como avaliar cor/tipo/forma, mas o próprio texto contraria a diretriz "mostrar em vez de adjetivar". |
| Distintividade | 1 | Trocando "Padaria do Zé" por qualquer padaria "gourmet" do mercado, o post continua fazendo sentido — não há nenhum elemento (nome de gente, endereço, tempo de fermentação, preço) que amarre a peça a esta marca. |

**Violações do DNA:**

1. Vocabulário proibido usado à vontade — DNA, seção 8:
   > "Nunca usamos: gourmet · experiência sensorial · premium · exclusivo · artesanal
   > sozinho como adjetivo vazio (só junto da prova de 24 horas) · notas, harmonização,
   > degustação · "sob consulta", "a partir de" sem número · "prezado cliente" ·
   > "reinventamos", "cara nova", "nova era" · "antigamente é que era bom" · nome do
   > concorrente em ataque direto"
   O post usa: "REINVENTADA", "Uma nova era", "linha gourmet de panetones premium",
   "harmonização exclusiva", "experiência sensorial", "sob consulta", "Prezado
   cliente", "linha premium exclusiva", "#gourmet #premium" e ataca a Trigo Dourado
   pelo nome ("melhores que os da Trigo Dourado").

2. Régua de decisão, item 1 — seção 11:
   > "Um freguês de 34 anos veria essa peça e concluiria que o preço continua o
   > mesmo? (Se a peça sugere upgrade, faixa nova ou "cara nova", reprovada.)"
   "PADARIA DO ZÉ REINVENTADA" / "Uma nova era começa" sugerem exatamente faixa
   nova e "cara nova" — reprovação automática por regra explícita.

3. Régua de decisão, item 3 — seção 11:
   > "Se há preço envolvido, o número está visível na peça? (Sem "sob consulta",
   > "a partir de" sem valor ou "chama no direct".)"
   A Tela 4 traz "Valores sob consulta no direct" — violação direta e nominal
   da própria régua.

4. Régua de decisão, item 4 — seção 11:
   > "A peça trata o leitor como vizinho ou como consumidor a ser convertido?
   > (Vizinho aprova; linguagem de funil, urgência artificial ou "clube" reprova.)"
   "Encomende já!", "Corra que é por tempo limitado" e "Garantimos" são
   linguagem de funil e urgência artificial.

5. Régua de decisão, item 5 — seção 11:
   > "A peça promete algo que a cozinha comprovadamente entrega hoje — volume,
   > prazo, variedade? (Enquanto o item 12.5 do briefing estiver aberto, qualquer
   > promessa de capacidade é reprovada por padrão.)"
   "Garantimos entrega em até 2 horas em qualquer endereço" é promessa de
   capacidade não sustentada — e o próprio DNA já sinaliza esse risco como
   **BLOQUEANTE** na tabela de Valores (seção 3): "**BLOQUEANTE:** ver briefing
   §12.5 (capacidade da cozinha desconhecida)."

6. Valor "O freguês antigo não é custo de aquisição" — seção 3:
   > "Reprovamos qualquer peça que sugira mudança de faixa de preço ou de
   > clientela."
   Toda a peça sugere upgrade de faixa ("linha gourmet premium", "reinventada"),
   contrariando esse valor.

7. Valor "Mostrar em vez de adjetivar" — seção 3:
   > "Não usamos banco de imagens, foto de produto que não saiu do nosso forno,
   > nem vocabulário sensorial de cardápio ("experiência", "notas amanteigadas").
   > Se não dá para provar, não entra na peça."
   O post é só adjetivo ("experiência sensorial única", "os melhores da
   região") sem nenhuma prova verificável (sem hora, sem endereço, sem foto,
   sem nome de quem atende).

8. Personalidade — seção 6, coluna "Não é":
   > "Arrogante, exclusivo, 'para quem entende'"
   "Nossos bolos são os melhores da região — melhores que os da Trigo Dourado,
   pode comparar" é comparação direta e arrogante, e nomear concorrente em
   ataque já está listado como vocabulário proibido (item 1 acima).

**Correções objetivas:**

1. Regularizar antes de tudo a Ficha de Aprovação do `dna-marca.md` (status
   `aprovado_cliente`) com o `gerente-de-contas` — nenhuma peça pode seguir
   enquanto o DNA não sair de `em_revisao`.
2. Remover "REINVENTADA" e "Uma nova era" da Tela 1; usar linguagem de
   continuidade, no modelo do próprio DNA: "Mudou a placa. O pão, o preço e o
   Marcos continuam iguais." (seção 7, reescritas de exemplo).
3. Reescrever a Tela 2 sem "gourmet", "premium", "harmonização", "exclusiva";
   substituir por prova concreta (tempo de fermentação, ingrediente real,
   processo do panetone).
4. Reescrever a Tela 3 sem "experiência sensorial" e sem comparação nominal
   com a Trigo Dourado; se houver comparação, deve ser indireta, como no
   posicionamento aprovado ("Duas quadras adiante cobram mais caro por um pão
   pior").
5. Substituir "Valores sob consulta no direct" por número exato de preço
   visível na peça (regra da régua de decisão item 3 e valor "Preço na
   parede").
6. Remover a promessa "entrega em até 2 horas em qualquer endereço" até o
   item 12.5 do briefing (capacidade da cozinha) ser resolvido; se mantida
   qualquer promessa de prazo, ela precisa vir confirmada com a Cláudia,
   conforme o valor "Encomenda combinada é encomenda cumprida".
7. Reescrever a legenda sem "Prezado cliente", sem "premium exclusiva", sem
   "sob medida" e sem "Corra que é por tempo limitado"; usar segunda pessoa
   coloquial ("a gente", nome de quem atende), conforme tom de voz (seção 7).
8. Trocar as hashtags #gourmet e #premium por termos do vocabulário permitido
   (ex.: #padariadobairro, #feitoaqui, #desde1992).
9. Incluir ao menos uma prova verificável por tela (hora que sai do forno,
   endereço, ano, ou nome de quem atende a encomenda), conforme régua de
   decisão item 2 e valor "Mostrar em vez de adjetivar".
