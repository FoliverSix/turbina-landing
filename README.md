# Turbina Soluções — Landing Page

Site institucional da Turbina Soluções. Apresenta os produtos **comerciais** do
ecossistema. Turbina Filmes e Turbina Música são projetos de uso pessoal e **não**
aparecem aqui.

## Produtos exibidos

| Produto | Status | Destino |
|---|---|---|
| Turbina Fit | Disponível | turbinafit.turbinasolucoes.com.br |
| Turbina Barber | Disponível | turbinabarber.turbinasolucoes.com.br |
| Turbina Academia | Em breve | — |
| Turbina Mercado | Em desenvolvimento | — |

## Stack

- HTML/CSS/JS estático, zero dependências de runtime
- Fonte Inter (Google Fonts)
- Docker + `nginx:alpine`

## Design System

Fonte única de verdade: `CLAUDE.md` na raiz dos projetos.

| Token | Valor |
|---|---|
| `--bg` | `#0D1117` |
| `--surface` / `--surface-2` | `#151B23` / `#1C2330` |
| `--border` / `--border-hover` / `--border-active` | `#1E2A36` / `#2A3441` / `#3A4A5A` |
| `--text` / `--text-2` / `--text-3` | `#E8EDF3` / `#8B95A1` / `#5A6474` |
| `--brand` (Turbina Soluções) | `#A78BFA` |
| `--fit` / `--academia` | `#22C55E` |
| `--barber` / `--barber-soft` | `#8B5E34` / `#D4A574` |
| `--mercado` | `#6366F1` |

`--brand` é identidade própria da marca-mãe e não herda cor de produto.
Botão primário: texto escuro (`#0D1117`) sobre fundo colorido — nunca branco.

## Estrutura

```
├── Dockerfile              # nginx:alpine + COPY html/
├── docker-compose.yml      # container turbina-landing, host :8180
├── nginx.conf              # cache, gzip, headers de segurança, MIME de SEO
├── html/                   # TUDO aqui dentro é publicado
│   ├── index.html
│   ├── termos.html
│   ├── privacidade.html
│   ├── robots.txt
│   ├── sitemap.xml
│   ├── favicon.ico         # 16/32/48/64
│   ├── favicon-32.png
│   ├── apple-touch-icon.png
│   ├── icon.svg
│   └── og-image.png        # 1200x630, Open Graph / Twitter Card
└── tools/                  # apenas geradores — NÃO vão para o container
    ├── og.html             # fonte do og-image.png
    └── icon.svg            # fonte dos favicons
```

## Links institucionais

- WhatsApp: `+55 22 99708-4278` → `https://wa.me/5522997084278`
- E-mail: `contato@turbinasolucoes.com.br`
- Documentos legais: `/termos.html` e `/privacidade.html` (redigidos para pessoa
  física, sem CNPJ/razão social — não há CNPJ)

## Deploy

O container roda na VM `144.22.173.196`. O host nginx faz proxy reverso para `:8180`.
Nada é buildado localmente (não há Docker nesta máquina).

```bash
# 1. Enviar o projeto para a VM (caminho DURÁVEL — /tmp é limpo no reboot)
cd "<pasta local>"
tar -czf - Dockerfile docker-compose.yml nginx.conf README.md html tools \
  | ssh ubuntu@144.22.173.196 'mkdir -p ~/turbina-landing && tar -xzf - -C ~/turbina-landing'

# 2. Build + restart na VM
ssh ubuntu@144.22.173.196 'cd ~/turbina-landing && docker compose up -d --build --force-recreate'

# 3. Verificar
curl -sI https://turbinasolucoes.com.br/ | head -1
curl -s -o /dev/null -w '%{http_code} %{content_type}\n' 'https://turbinasolucoes.com.br/favicon.ico?v=2'
# conferir que a URL limpa do HTML serve o arquivo NOVO (nao a copia do edge):
curl -s -o /dev/null -w 'servido=%{size_download} local=%{size_upload}\n' 'https://turbinasolucoes.com.br/favicon-32.png?v=2'
stat -c 'local=%s' html/favicon-32.png
```

Rollback: antes de cada deploy, a imagem atual é tagueada como
`turbina-landing:rollback-AAAAMMDD-HHMM`.

## Regenerar os assets (favicon + og-image)

Requer Chrome/Edge e Pillow. Gera `html/og-image.png`, `html/favicon.ico`,
`html/favicon-32.png` e `html/apple-touch-icon.png` a partir de `tools/`.

```bash
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
OUT="C:/Users/<user>/AppData/Local/Temp/chrshot"; mkdir -p "$OUT"

# og-image 1200x630 (aguarda o Chrome terminar antes de usar o arquivo)
timeout 60 "$CHROME" --headless=new --disable-gpu --no-sandbox --user-data-dir="$OUT/p1" \
  --hide-scrollbars --virtual-time-budget=9000 --window-size=1200,630 \
  --screenshot="$OUT/og.png" "file:///<caminho>/tools/og.html"
sleep 10

# icone 512x512 com fundo TRANSPARENTE (sem esta flag os cantos saem brancos)
timeout 60 "$CHROME" --headless=new --disable-gpu --no-sandbox --user-data-dir="$OUT/p2" \
  --hide-scrollbars --virtual-time-budget=4000 --default-background-color=00000000 \
  --window-size=512,512 --screenshot="$OUT/icon.png" "file:///<caminho>/tools/icon.svg"
sleep 8
```

Depois, com Pillow: recortar `og.png` → `og-image.png`; `icon.png` →
`favicon.ico` (sizes `16/32/48/64`), `favicon-32.png` e `apple-touch-icon.png` (180, RGB).

## Notas

- `/sitemap.xml` e `/robots.txt` são servidos com `default_type` próprio para não
  caírem no `try_files /index.html`.
- O Cloudflare injeta um bloco gerenciado no topo do `robots.txt`; o conteúdo do
  repositório é anexado ao final.
- HTML sai com `Cache-Control: no-cache` — atualização é imediata.
- Ícones usam nome fixo, por isso ficam com cache curto (`1h`, `must-revalidate`) **e são
  versionados no HTML** (`/favicon.ico?v=2`). Ao mexer em qualquer ícone, **suba o `?v=` nos três
  HTMLs** (`index.html`, `termos.html`, `privacidade.html`); senão o edge do Cloudflare segue
  servindo a cópia antiga por dias.
- **O cache do Cloudflare não é o cache do navegador, e um sobrevive ao outro.** A zona está com
  *Browser Cache TTL* em 4h, que sobrescreve o `max-age` do nginx. Resultado: com a origem já
  atualizada, o edge continua entregando o arquivo velho. Para flagrar isso, compare o
  `content-length` da resposta **limpa** com o do arquivo local e olhe `cf-cache-status` + `Age` —
  `HIT` com `Age` grande é cópia velha. Se precisar forçar agora, purgue aquela URL no painel do
  Cloudflare (Caching → Configuration → Purge by URL).
- **NUNCA valide asset com `?cb=<timestamp>`.** Cada query string é uma chave de cache nova, então o
  Cloudflare sempre vai à origem e devolve o arquivo certo — foi assim que uma primeira verificação
  "passou" com o favicon antigo preso no edge. Valide sempre com a URL exata que o HTML usa.
