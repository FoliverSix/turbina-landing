# Turbina Soluções — Prompts para gerar símbolo, logo e favicon

## Regra de ouro

Gerador de imagem **não** entrega favicon pronto. Ele entrega um **símbolo raster**.
O fluxo que funciona:

```
IA (símbolo, 1024x1024)
   -> recorte / limpeza de fundo
   -> vetorização (SVG)  <- aqui o símbolo vira crispal de verdade
   -> wordmark "TURBINA SOLUÇÕES" em Inter ExtraBold (texto NUNCA via IA)
   -> render PNG: favicon.ico 16/32/48/64, apple-touch-icon 180, og-image 1200x630
```

Motivo: IA erra acento ("SOLUÇÕES" sai "SOLUCOES"/"SOLUCÕES"), erra kerning e
não desenha circunferência perfeita. Símbolo sim, texto não.

## Constantes da marca (não mudam)

| Item | Valor |
|---|---|
| Cor de acento | `#A78BFA` (lavanda) |
| Fundo | `#0D1117` |
| Texto sobre acento | `#0D1117` (nunca branco) |
| Fonte do wordmark | Inter, peso 800, letter-spacing -0.03em |
| Acento dos produtos | Fit `#22C55E` · Barber `#8B5E34` · Mercado `#6366F1` |

`#A78BFA` é identidade própria da marca-mãe — não herda cor de produto.

---

## 1. PROMPT DO SÍMBOLO (base — use este para o favicon)

Escreva em **inglês**: Midjourney, Flux e SDXL rendem visivelmente melhor, e o
resultado não muda por ser outro idioma.

```
Minimal flat vector logo mark for a software company. A single abstract
symbol inspired by a turbine impeller: six identical curved blades
radiating symmetrically from a solid circular hub, drawn with thick
uniform strokes and generous negative space between the blades.

Single flat color: vivid lavender purple #A78BFA.
Background: flat solid dark charcoal #0D1117.

Perfectly centered, square 1:1 composition, about 15% empty padding on
all four sides. Strictly flat 2D vector, crisp clean edges, geometric
and symmetrical.

No gradients. No shading. No 3D. No bevel. No drop shadow. No glow.
No outer outline. No texture. No text. No letters. No words. No numbers.
No mockup. No device frame. No watermark. No signature.

Brand identity design, app icon, simple enough to stay perfectly legible
when scaled down to a 16x16 pixel favicon.
```

### Negative prompt (campos `--no` do Midjourney, ou negative no Flux/SDXL)

```
text, letters, words, numbers, typography, watermark, signature, gradient,
gradient mesh, 3d, render, realistic, photo, bevel, emboss, drop shadow,
glow, neon, texture, grain, noise, thin lines, fine detail, hairline,
multiple symbols, collage, grid, frame, border, mockup, device, tshirt,
busy, cluttered, asymmetric, blurry, low contrast
```

### Variações — troque só o trecho do motivo

- **Pás de turbina (recomendado)** — `six identical curved blades radiating symmetrically from a solid circular hub`
- **Monograma T** — `a bold geometric letter T cut by two angled turbine blades, negative space forming the blades`
- **Camadas (atual do site)** — `three stacked chevron layers, the top one solid and the two below as thick outlines`
- **Vórtice** — `a spiral of three tapered blades converging into a single point at the center`

### Por que "16x16" aparece no prompt

É o teste que elimina 90% dos candidatos. Se o símbolo precisa de detalhe fino
para ser entendido, ele morre no favicon. Blades grossas + vazio generoso = sobrevive.

---

## 1-B. Versão dedicada — GPT Image (ChatGPT)

`gpt-image-1` não aceita negative prompt nem flags: as exclusões vão **em prosa**
("Do not include..."), e ele obedece bem. Também é multilíngue — aceita português
sem perda. Mantenha em inglês só por consistência.

Cole isto no ChatGPT **em uma mensagem só**, junto com a trava do fim:

```
Create exactly one single square logo mark image for a software company.

Subject: one abstract symbol inspired by a turbine impeller — six identical
curved blades radiating symmetrically from a solid circular hub. Thick uniform
strokes. Generous empty space between the blades so the shape stays instantly
readable at tiny sizes.

Color: the symbol is one single flat lavender purple, exactly #A78BFA. No other
color anywhere in the symbol.

Background: one flat solid dark charcoal, exactly #0D1117. Completely uniform —
no vignette, no radial glow, no texture, no subtle gradient.

Composition: perfectly centered on a square 1:1 canvas. The symbol occupies about
70% of the width, leaving roughly 15% empty padding on all four sides. Strictly
symmetrical across both axes.

Style: flat 2D vector illustration, like a professional SVG logo. Crisp edges,
geometric precision, solid fills.

Do not include any text, letters, words, numbers, or typography of any kind.
Do not include gradients, shading, highlights, 3D, bevel, emboss, drop shadow,
glow, an outer outline around the shape, texture, grain, or noise. Do not include
a watermark, a signature, a logo mockup, a business card, a device frame, a
presentation board, a grid or collage of variations, or any decorative background
element.

One single logo mark on the solid background. Nothing else in the frame.

This is a favicon source asset: it must remain perfectly legible when scaled down
to 16x16 pixels.

Generate exactly the image described above. Do not rewrite, summarize, or "improve"
this prompt, and do not ask clarifying questions — generate the image now.
```

### As três travas que só o GPT Image precisa

**"Do not rewrite this prompt"** — o ChatGPT tende a resumir/reescrever o pedido
antes de gerar e perde as exclusões. É a última linha do bloco acima, não remova.

**"exactly one single"** + **"no grid or collage"** — o comportamento padrão dele é
devolver grade 2x2 de variações e um mockup em camiseta/cartão de visita. Essas duas
frases cortam isso.

**"square 1:1 canvas"** — sem isso ele entrega paisagem. No app do ChatGPT vale
escrever "quadrada" também.

Transparência: o ChatGPT não dá canal alfa confiável. Via API, `gpt-image-1` tem
`background: "transparent"` + `output_format: "png"` — aí sai com alfa real. Fora
isso, peça fundo chapado e o fundo é removido depois.

Sobre texto: o `gpt-image-1` é bem melhor com tipografia que o DALL·E 3 — o lockup
fica viável como referência. Ainda erra acento; o "Õ" de "SOLUÇÕES" é o ponto de
falha típico. Confira letra por letra.

---

## 2. PROMPT DO LOGO COMPLETO (lockup)

Use quando quiser **uma referência visual** de como símbolo + nome se relacionam.
O arquivo final ainda deve ser montado em SVG.

```
Minimal flat vector logo lockup for a software company called TURBINA.
Left: a small abstract symbol inspired by a turbine impeller, six curved
blades radiating from a solid hub, thick uniform strokes, lavender purple
#A78BFA.

Right: the wordmark "TURBINA" in extra-bold geometric sans-serif
(Inter ExtraBold / Poppins ExtraBold style), tight letter spacing, all
caps, same lavender purple #A78BFA.

Below the wordmark, a small lighter-grey line reading "SOLUÇÕES" in
medium weight, uppercase, wide letter spacing.

Background: flat solid dark #0D1117. Horizontal composition, generous
margin. Strictly flat 2D vector. No gradients, no 3D, no shadow, no glow,
no texture, no mockup, no extra decoration.
```

Aviso: mesmo Ideogram e GPT-Image vão errar "SOLUÇÕES" com alguma frequência.
Considere a saída como **referência de proporção**, não como arquivo final.

---

## 3. PROMPT DE APP ICON (iOS / Android / PWA)

```
Flat vector app icon, 1024x1024, rounded square tile with corner radius
about 22% of the side. Solid lavender purple #A78BFA tile. Centered on
the tile, a dark charcoal #0D1117 abstract turbine impeller symbol: six
curved blades radiating from a solid hub, thick uniform strokes,
generous negative space, perfectly symmetrical, occupying about 60% of
the tile width.

Flat 2D, crisp vector edges. No gradient, no gloss, no 3D, no inner
shadow, no drop shadow, no border, no text, no letters, no mockup, no
device frame.
```

---

## 4. Adaptadores por ferramenta

Cole o prompt base e ajuste só o final.

**Midjourney (v7)**
```
<prompt base> --ar 1:1 --style raw --stylize 100 --no text, letters, gradient, 3d, shadow, mockup, watermark
```
`--style raw` e `--stylize 100` (baixo) são o que impedem o MJ de "artisticar"
um logo. Estilização alta enche de detalhe e destrói o uso em 16px.

**Flux / SDXL / ComfyUI (local)**
- CFG 4.5–6 (alto demais satura e cria detalhe fino)
- Steps 28–35
- Sampler `dpmpp_2m` + scheduler `karras`
- Resolução 1024x1024 (não 512 — símbolo geométrico precisa de resolução)
- Coloque o negative prompt no nó de negative, não no positivo

**DALL·E 3 / GPT Image / Gemini**
Aceita português, mas mantenha em inglês pela consistência do vocabulário visual.
Peça explicitamente: *"apenas o símbolo, não gere variações em grade"*.
Para GPT Image, use o bloco pronto da **seção 1-B** — ele é mais específico do que
adaptar o prompt base.

**Ideogram** — o melhor para o lockup com texto (acentos inclusos no v3).
Ainda assim, confira "SOLUÇÕES" letra por letra.

**Recraft** — se for usar nuvem, é o mais indicado: gera **SVG de verdade**,
o que pula a etapa de vetorização.

---

## 5. Checklist depois de gerar

1. Reduza para 32x32 e depois 16x16. Continua reconhecível? Se não, descarte.
2. Veja em escala de cinza. Se depende só de cor para ser entendido, o símbolo é fraco.
3. Confira se o símbolo é simétrico de verdade (gerador quase sempre entrega levemente torto).
4. Teste sobre `#0D1117` **e** sobre `#FFFFFF` (a og-image e o e-mail podem ser claros).
5. Só então vetorize → `html/icon.svg` → regenere o conjunto (ver README > "Regenerar os assets").

---

## 6. Atalho sem IA

Se quiser algo pronto hoje, os prompts acima são a **direção** — mas o símbolo
de camadas que já está em `html/icon.svg` resolve. É geométrico, simétrico,
sobrevive a 16px e usa a cor da marca. Um símbolo de turbina seria mais
"Turbina", porém com risco de virar genérico (roda dentada / hélice de ventilador).
