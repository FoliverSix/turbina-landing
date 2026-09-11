# Turbina Soluções — Prompts para gerar símbolo, logo e favicon

## 0. O que a marca realmente é

Antes de qualquer prompt: **a identidade da Turbina não é uma turbina.** É um
**glifo de camadas empilhadas** sobre um tile quadrado arredondado.

Está em `html/icon.svg`, e o mesmo `<path>` aparece no navbar (linha 560) e no
rodapé (linha 756) do `index.html`:

```
<rect width="64" height="64" rx="14" fill="#A78BFA"/>
<path d="M12 2L2 7l10 5 10-5-10-5z" fill="#0D1117"/>        <- losango solido em cima
<path d="M2 17l10 5 10-5" stroke="#0D1117" stroke-width="2.5"/>   <- chevron 1
<path d="M2 12l10 5 10-5" stroke="#0D1117" stroke-width="2.5"/>   <- chevron 2
```

Traduzindo: **losango sólido em cima, dois chevrons de espessura idêntica
embaixo**, tudo em `#0D1117` sobre tile `#A78BFA` com raio de canto ≈22% do lado.

Os quatro produtos repetem exatamente o mesmo sistema — tile `rx=14`, glifo escuro
`#0D1117`, e só mudam a cor do tile e o desenho:

| Produto | Cor do tile | Glifo |
|---|---|---|
| Turbina (marca-mãe) | `#A78BFA` | camadas empilhadas |
| TurbinaFit | `#22C55E` | letra T |
| TurbinaBarber | `#8B5E34` | tesoura |
| Turbina Academia | `#22C55E` | barras de gráfico |
| Turbina Mercado | `#6366F1` | sacola de compras |

**Consequência prática:** um símbolo de turbina/hélice não pertence a esta marca.
Já foi tentado e destoa — parece ventilador, roda de cassino ou hélice genérica, e
não conversa com nenhum dos quatro produtos. Se algum prompt devolver pás girando,
ele está errado.

---

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

Motivo: IA erra acento ("SOLUÇÕES" sai "SOLUCOES"/"SOLUCÕES"), erra kerning e não
desenha circunferência perfeita. Símbolo sim, texto não.

**Aviso importante:** o `icon.svg` atual já é vetor limpo, simétrico e na cor
exata. Para *reproduzir* essa marca, IA é a ferramenta errada — ela só vai
introduzir assimetria, borda borrada e hex fora do tom. IA serve para **evoluir**
o desenho (seção 7), não para refazer o que já está correto.

## Constantes da marca (não mudam)

| Item | Valor |
|---|---|
| Cor de acento | `#A78BFA` (lavanda) |
| Fundo | `#0D1117` |
| Glifo sobre tile colorido | `#0D1117` (nunca branco) |
| Raio de canto do tile | ≈22% do lado (`rx=14` em 64) |
| Fonte do wordmark | Inter, peso 800, letter-spacing -0.03em |
| Acento dos produtos | Fit `#22C55E` · Barber `#8B5E34` · Mercado `#6366F1` · Academia `#22C55E` |

`#A78BFA` é identidade própria da marca-mãe — não herda cor de produto.

---

## 1. PROMPT BASE DO SÍMBOLO (o motivo é camadas, não turbina)

Escreva em **inglês**: Midjourney, Flux e SDXL rendem visivelmente melhor, e o
resultado não muda por ser outro idioma.

```
Minimal flat vector logo mark for a software company. A single abstract
symbol of three stacked layers: a solid diamond shape at the top, with two
evenly spaced V-shaped chevrons of identical thickness below it, the whole
thing perfectly aligned and centered. Generous negative space between the
layers.

Single flat color for the symbol: dark charcoal #0D1117.
Tile behind it: one flat solid lavender purple #A78BFA, rounded square with
corner radius about 22% of its side.
Background outside the tile: one flat solid pure white #FFFFFF, uniform.

Composition: tile centered on a square 1:1 canvas with about 6% empty margin
on all sides. The glyph occupies about 60% of the tile width.

Strictly flat 2D vector, crisp clean edges, geometric and symmetrical.

No gradients. No shading. No 3D. No bevel. No drop shadow. No glow.
No outer outline. No texture. No text. No letters. No words. No numbers.
No mockup. No device frame. No watermark. No signature.

App icon design, simple enough to stay perfectly legible when scaled down to
a 16x16 pixel favicon.
```

### Negative prompt (campo `--no` do Midjourney, ou negative no Flux/SDXL)

```
text, letters, words, numbers, typography, watermark, signature, gradient,
gradient mesh, 3d, render, realistic, photo, bevel, emboss, drop shadow,
glow, neon, texture, grain, noise, thin lines, fine detail, hairline,
turbine, propeller, fan blades, pinwheel, spiral, multiple symbols, collage,
grid, frame, border, mockup, device, busy, cluttered, asymmetric, blurry,
low contrast
```

Repare que `turbine, propeller, fan blades, pinwheel` estão no negative de
propósito: é o erro mais provável de acontecer de novo.

### Variações — troque só o trecho do motivo

- **Camadas empilhadas (a marca atual)** — `a solid diamond on top with two evenly spaced V-shaped chevrons below it`
- **Monograma T em camadas** — `a bold geometric letter T built from three stacked horizontal layers`
- **Camadas em isométrico** — `three identical flat rhombus plates stacked with even spacing, seen at a slight isometric angle`
- **Três placas com contorno** — `three stacked chevron layers, the top one solid and the two below as thick outlines`

### Por que "16x16" aparece no prompt

É o teste que elimina 90% dos candidatos. Se o símbolo precisa de detalhe fino
para ser entendido, ele morre no favicon. Formas grossas + vazio generoso = sobrevive.

---

## 1-B. Versão dedicada — GPT Image (ChatGPT)

`gpt-image-1` não aceita negative prompt nem flags: as exclusões vão **em prosa**
("Do not include..."), e ele obedece bem. Também é multilíngue — aceita português
sem perda. Mantenha em inglês só por consistência.

Cole isto no ChatGPT **em uma mensagem só**:

```
Create exactly one single square app-icon image for a software company.

Subject: a flat minimal glyph of three stacked layers. At the top, a solid
diamond shape. Below it, two evenly spaced V-shaped chevrons of identical
thickness, aligned to the same width as the diamond, receding downward. The
whole glyph is perfectly centered and symmetrical, with generous empty space
between the layers.

Colors: the glyph is one single flat dark charcoal, exactly #0D1117. It sits
inside a filled rounded square tile of one single flat lavender purple, exactly
#A78BFA. Outside the tile, the background is one flat solid pure white #FFFFFF,
completely uniform.

Composition: a rounded square tile whose corner radius is about 22% of its side.
The tile is centered on a square 1:1 canvas with about 6% empty margin on all
sides. The glyph occupies about 60% of the tile width.

Style: flat 2D vector, like a professional SVG app icon. Crisp edges, geometric
precision, solid fills, uniform stroke thickness, strict symmetry.

Do not include any text, letters, words, numbers, or typography of any kind.
Do not include gradients, shading, highlights, 3D, bevel, emboss, perspective,
drop shadow, glow, or an outer outline around the tile, texture, grain, or noise.
Do not include any turbine, propeller, fan blade, pinwheel or spiral shape.
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
devolver grade 2x2 de variações e um mockup em camiseta/cartão de visita. Essas duas
frases cortam isso.

**"square 1:1 canvas"** — sem isso ele entrega paisagem. No app do ChatGPT vale
escrever "quadrada" também.

**Por que o fundo externo é branco puro:** o `icon.svg` real não tem fundo — só o
tile roxo com cantos transparentes. Pedindo o branco chapado, é possível remover o
fundo depois com um simples key de cor (nem o tile `#A78BFA` nem o glifo `#0D1117`
são brancos, então o recorte sai limpo). Se pedir fundo escuro, o glifo e o fundo
viram a mesma cor e não há como separar.

Transparência: o ChatGPT não dá canal alfa confiável. Via API, `gpt-image-1` tem
`background: "transparent"` + `output_format: "png"` — aí sai com alfa real.

Sobre texto: o `gpt-image-1` é bem melhor com tipografia que o DALL·E 3 — o lockup
fica viável como referência. Ainda erra acento; o "Õ" de "SOLUÇÕES" é o ponto de
falha típico. Confira letra por letra.

---

## 2. PROMPT DO LOGO COMPLETO (lockup)

Use quando quiser **uma referência visual** de como símbolo + nome se relacionam.
O arquivo final ainda deve ser montado em SVG.

```
Minimal flat vector logo lockup for a software company called TURBINA.
Left: a small app-icon tile, rounded square with corner radius about 22% of
its side, filled flat lavender purple #A78BFA, containing a dark charcoal
#0D1117 glyph of three stacked layers — a solid diamond on top with two
evenly spaced V-shaped chevrons below.

Right: the wordmark "TURBINA" in extra-bold geometric sans-serif
(Inter ExtraBold / Poppins ExtraBold style), tight letter spacing, all
caps, lavender purple #A78BFA.

Below the wordmark, a small lighter-grey line reading "SOLUÇÕES" in
medium weight, uppercase, wide letter spacing.

Background: flat solid dark #0D1117. Horizontal composition, generous
margin. Strictly flat 2D vector. No gradients, no 3D, no shadow, no glow,
no texture, no mockup, no turbine or propeller shapes, no extra decoration.
```

Aviso: mesmo Ideogram e GPT-Image vão errar "SOLUÇÕES" com alguma frequência.
Considere a saída como **referência de proporção**, não como arquivo final.

---

## 3. PROMPT DE APP ICON (iOS / Android / PWA)

```
Flat vector app icon, 1024x1024, rounded square tile with corner radius
about 22% of the side. Solid lavender purple #A78BFA tile. Centered on
the tile, a dark charcoal #0D1117 glyph of three stacked layers: a solid
diamond on top with two evenly spaced V-shaped chevrons of identical
thickness below it, occupying about 60% of the tile width and perfectly
symmetrical.

Background outside the tile: flat solid pure white #FFFFFF.
Flat 2D, crisp vector edges. No gradient, no gloss, no 3D, no inner
shadow, no drop shadow, no border, no text, no letters, no mockup, no
device frame, no turbine or propeller shapes.
```

---

## 4. Adaptadores por ferramenta

Cole o prompt base da seção 1 e ajuste só o final.

**Midjourney (v7)**
```
<prompt base> --ar 1:1 --style raw --stylize 100 --no text, letters, gradient, 3d, shadow, mockup, watermark, turbine, propeller, fan blades
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
4. Confira se o hex é exatamente `#A78BFA` / `#0D1117` — gerador quase sempre
   entrega um tom vizinho. Ajuste na mão antes de usar.
5. Teste sobre `#0D1117` **e** sobre `#FFFFFF`.
6. Só então vetorize → `html/icon.svg` → regenere o conjunto (ver README > "Regenerar os assets").

---

## 6. Se o objetivo for só ter o favicon funcionando

Não use IA. O `html/icon.svg` já é o certo: vetor, simétrico, na cor exata, e
sobrevive a 16px. Um gerador de imagem vai *piorar* esse arquivo, não melhorar.

IA entra apenas quando a decisão for **redesenhar** a marca — e aí o motivo tem que
continuar sendo camadas, porque é isso que amarra os quatro produtos entre si.

---

## 7. Se quiser evoluir o desenho (sem trocar o motivo)

Três direções que continuam dentro do sistema atual:

- **Camadas em isométrico** — as três placas ganham leve perspectiva, dando
  profundidade sem sair do flat. Mais "software" que o atual.
- **Camadas com o vão maior** — aumentar o espaço entre as placas melhora a
  leitura em 16px, hoje o chevron de baixo quase encosta no do meio.
- **Monograma T em camadas** — o T construído por três faixas horizontais: fica
  mais próprio da Turbina que o glifo genérico de camadas (que é idêntico ao
  ícone `layers` do Lucide/Feather, usado por milhares de projetos).

A terceira é a que mais resolve o problema real: o glifo atual **não é original**,
é o `layers` do Lucide. Funciona, mas não distingue a marca de nada.
