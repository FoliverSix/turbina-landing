# Turbina Soluções — Prompts para gerar símbolo, logo e favicon

> Previews renderizados em `tools/logo-drafts/` (`preview-finalistas.png`).
> Rascunhos em SVG: `HA.svg`, `HB.svg`, `HC.svg`, `HF.svg`.

## 0. O que foi testado (leia antes de gerar)

Duas rodadas de rascunho, avaliadas rasterizadas de verdade em 16px e 32px:

| Tentativa | O que deu | 16px |
|---|---|---|
| Rotor 5 pás (gerado por IA) | Parece hélice de ventilador / roda de cassino | Borrão |
| Rotor 3 pás, cunha | Parece "Y" torto | Borrão |
| Rotor 3 pás, reto | Parece hélice de lancha / estrela ninja | Borrão |
| Rotor com anel externo | Parece grade de ventilador ou relógio | Borrão |
| Virgulas / crescentes | Parece símbolo de radiação | Borrão |
| **Monograma T** | **Lê como letra T na hora** | **Legível** |

**Conclusão: um rotor literal não sobrevive a 16px.** Três ou cinco pás dentro de
um círculo perdem a leitura quando o ícone tem 16 pixels de lado — viram mancha.
O que sobrevive é a letra **T**, que é o inicial do nome e tem silhueta simples.

O caminho que resolve as duas coisas: **um T cujas pontas da barra são pás de
turbina.** Em 256px lê-se "T com movimento"; em 16px lê-se "T". É o `HF.svg`.

### O que a marca é hoje

O `html/icon.svg` em produção é o ícone `layers` do Lucide (losango sólido + dois
chevrons) sobre tile `#A78BFA`. Funciona, mas é genérico. O mesmo path aparece no
navbar (linha 560) e no rodapé (linha 756) do `index.html`.

Os quatro produtos repetem o sistema — tile arredondado colorido + glifo escuro
`#0D1117`, mudando só a cor e o desenho: Fit `#22C55E` (letra T), Barber `#8B5E34`
(tesoura), Academia `#22C55E` (barras), Mercado `#6366F1` (sacola).

**Qualquer símbolo novo para a marca-mãe deve manter esse sistema**: tile `rx=14`
(≈22% do lado) + glifo `#0D1117`. Só o desenho dentro do tile muda.

---

## Regra de ouro

Gerador de imagem **não** entrega favicon pronto. Ele entrega um **símbolo raster**.
O fluxo que funciona:

```
IA (símbolo, 1024x1024)
   -> recorte / limpeza de fundo
   -> vetorização (SVG)
   -> wordmark "TURBINA SOLUÇÕES" em Inter ExtraBold (texto NUNCA via IA)
   -> render PNG: favicon.ico 16/32/48/64, apple-touch-icon 180, og-image 1200x630
```

Motivo: IA erra acento ("SOLUÇÕES" sai "SOLUCOES"), erra kerning e não desenha
geometria exata. Símbolo sim, texto não.

## Constantes da marca (não mudam)

| Item | Valor |
|---|---|
| Cor de acento | `#A78BFA` (lavanda) |
| Fundo | `#0D1117` |
| Glifo sobre tile colorido | `#0D1117` (nunca branco) |
| Raio de canto do tile | ≈22% do lado (`rx=14` em 64) |
| Fonte do wordmark | Inter, peso 800, letter-spacing -0.03em |
| Acento dos produtos | Fit `#22C55E` · Barber `#8B5E34` · Mercado `#6366F1` · Academia `#22C55E` |

---

## 1. PROMPT RECOMENDADO — monograma T com pontas de pá

O conceito: um T cuja barra horizontal tem as pontas afinando e varrendo para
baixo, como as pontas de uma pá de turbina. A haste é vertical, reta, afinando
levemente.

```
Minimal flat vector app-icon mark for a software company. A bold geometric
monogram of the capital letter T: a horizontal crossbar whose two ends taper
and sweep downward like the tips of turbine blades, with a vertical stem
slightly narrower at the bottom, centered beneath the crossbar. Perfectly
symmetrical, even visual weight between crossbar and stem.

The T is one single flat dark charcoal, exactly #0D1117.
The T sits inside a filled rounded square tile of one single flat lavender
purple, exactly #A78BFA.
Outside the tile: one flat solid pure white #FFFFFF, completely uniform.

Composition: rounded square tile, corner radius about 22% of its side,
centered on a square 1:1 canvas with about 6% empty margin on all sides.
The T occupies about 62% of the tile width and is perfectly centered.

Strictly flat 2D vector, crisp clean edges, geometric precision, solid fills,
uniform stroke thickness.

No gradients. No shading. No 3D. No bevel. No drop shadow. No glow.
No outer outline. No texture. No mockup. No device frame. No watermark.
No full turbine rotor. No propeller. No fan wheel. No pinwheel. No spiral.

Simple enough to stay perfectly legible when scaled down to a 16x16 pixel
favicon.
```

### Negative prompt (`--no` do Midjourney, ou negative no Flux/SDXL)

```
turbine rotor, propeller, fan wheel, fan blades, pinwheel, spiral, helix,
gradient, gradient mesh, 3d, render, realistic, photo, bevel, emboss,
drop shadow, glow, neon, texture, grain, noise, thin lines, fine detail,
hairline, serif letter, lowercase, other letters, words, numbers, watermark,
signature, mockup, device, busy, cluttered, asymmetric, blurry, low contrast
```

`turbine rotor, propeller, fan wheel, pinwheel` estão no negative de propósito:
é o erro mais provável. O T tem que ser um T, não um cata-vento.

---

## 1-B. Versão dedicada — GPT Image (ChatGPT)

`gpt-image-1` não aceita negative prompt nem flags: as exclusões vão **em prosa**
("Do not include..."). Cole isto no ChatGPT **em uma mensagem só**:

```
Create exactly one single square app-icon image for a software company.

Subject: a bold geometric monogram of the capital letter T. The crossbar is a
horizontal bar whose two ends taper and sweep downward like the tips of turbine
blades. The stem is a vertical bar, slightly narrower at the bottom, centered
beneath the crossbar. The letter is perfectly symmetrical, with even visual
weight between the crossbar and the stem.

Colors: the letter T is one single flat dark charcoal, exactly #0D1117. It sits
inside a filled rounded square tile of one single flat lavender purple, exactly
#A78BFA. Outside the tile, the background is one flat solid pure white #FFFFFF,
completely uniform.

Composition: a rounded square tile whose corner radius is about 22% of its side.
The tile is centered on a square 1:1 canvas with about 6% empty margin on all
sides. The letter T occupies about 62% of the tile width and is perfectly centered.

Style: flat 2D vector, like a professional SVG app icon. Crisp edges, geometric
precision, solid fills, strict symmetry, uniform stroke thickness.

Do not include any letters, words, numbers or typography other than the single
capital letter T.
Do not include gradients, shading, highlights, 3D, bevel, emboss, perspective,
drop shadow, glow, or an outer outline around the tile, texture, grain, or noise.
Do not include a full turbine rotor, a propeller, a fan wheel, fan blades, a
pinwheel, a spiral or any wheel with several blades.
Do not include a watermark, a signature, a logo mockup, a business card, a device
frame, a presentation board, a grid or collage of variations, or any decorative
background element.

One single app-icon tile on a plain flat background. Nothing else in the frame.

This is a favicon source asset: it must remain perfectly legible when scaled down
to 16x16 pixels.

Generate exactly the image described above. Do not rewrite, summarize, or "improve"
this prompt, and do not ask clarifying questions — generate the image now.
```

### As três travas que só o GPT Image precisa

**"Do not rewrite this prompt"** — o ChatGPT tende a resumir/reescrever o pedido
antes de gerar e perde as exclusões. É a última linha do bloco acima, não remova.

**"exactly one single"** + **"no grid or collage"** — o comportamento padrão dele é
devolver grade 2x2 de variações e um mockup em camiseta/cartão de visita.

**"square 1:1 canvas"** — sem isso ele entrega paisagem.

**Por que o fundo externo é branco puro:** o ícone real não tem fundo — só o tile
roxo com cantos transparentes. Pedindo branco chapado, dá para remover o fundo
depois com um key de cor simples (nem `#A78BFA` nem `#0D1117` são brancos). Com
fundo escuro, o glifo e o fundo viram a mesma cor e não há como separar.

**Risco específico deste prompt:** o `gpt-image-1` lê "turbine blade tips" e pode
converter o T inteiro num rotor. Se acontecer, remova a menção a "turbine blades" e
peça só "a bold geometric T with tapered ends that curve slightly downward".

---

## 2. PROMPT DO LOGO COMPLETO (lockup)

Referência de proporção — o arquivo final deve ser montado em SVG.

```
Minimal flat vector logo lockup for a software company called TURBINA.
Left: a small app-icon tile, rounded square with corner radius about 22% of
its side, filled flat lavender purple #A78BFA, containing a dark charcoal
#0D1117 monogram of the capital letter T whose crossbar ends taper and sweep
downward like turbine blade tips.

Right: the wordmark "TURBINA" in extra-bold geometric sans-serif
(Inter ExtraBold style), tight letter spacing, all caps, lavender purple #A78BFA.

Below the wordmark, a small lighter-grey line reading "SOLUÇÕES" in medium
weight, uppercase, wide letter spacing.

Background: flat solid dark #0D1117. Horizontal composition, generous margin.
Strictly flat 2D vector. No gradients, no 3D, no shadow, no glow, no texture,
no mockup, no full turbine rotor, no extra decoration.
```

---

## 3. Adaptadores por ferramenta

**Midjourney (v7)**
```
<prompt base da secao 1> --ar 1:1 --style raw --stylize 100 --no turbine rotor, propeller, fan wheel, pinwheel, spiral, gradient, 3d, shadow, mockup, watermark
```
`--style raw` e `--stylize 100` (baixo) impedem o MJ de "artisticar". Estilização
alta enche de detalhe e destrói o uso em 16px.

**Flux / SDXL / ComfyUI (local)**
- CFG 4.5–6 · steps 28–35 · `dpmpp_2m` + `karras` · 1024x1024
- Negative no nó de negative, não no positivo

**DALL·E 3 / GPT Image / Gemini** — para GPT Image use o bloco pronto da seção 1-B.

**Ideogram** — melhor para o lockup com texto. Ainda assim confira "SOLUÇÕES".

**Recraft** — gera SVG de verdade, pula a vetorização.

---

## 4. Checklist depois de gerar

1. Rasterize de verdade em 16x16 (não escale o SVG — abra num viewport de 16px).
   Continua legível? Se não, descarte. Foi exatamente este passo que reprovou todos
   os rotores.
2. Confira se o hex é exatamente `#A78BFA` / `#0D1117` — gerador quase sempre
   entrega um tom vizinho.
3. Confira simetria (gerador quase sempre entrega levemente torto).
4. Teste sobre `#0D1117` **e** sobre `#FFFFFF`.
5. Só então vetorize → `html/icon.svg` → regenere todo o conjunto (ver README >
   "Regenerar os assets").

---

## 5. Composição final e atalho sem IA

O wordmark nunca sai da IA: "TURBINA" + "SOLUÇÕES" em Inter ExtraBold, montado em
SVG. A IA fornece só o símbolo.

E se o objetivo for apenas ter o favicon redondo e funcionando hoje, o
`tools/logo-drafts/HF.svg` já é vetor limpo, simétrico, na cor exata, e passa no
teste de 16px. Não precisa de gerador de imagem nenhum.
