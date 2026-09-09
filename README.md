# Turbina Soluções — Landing Page

Landing page institucional da Turbina Soluções, apresentando todos os produtos da plataforma.

## Produtos

- **Turbina Fit** — Gestão para personal trainers
- **Turbina Barber** — Gestão para barbearias
- **Turbina Academia** — Gestão para academias (em breve)
- **Turbina Mercado** — Marketplace (em desenvolvimento)

## Stack

- HTML/CSS/JS (static, zero dependencies)
- Inter font (Google Fonts)
- Docker + nginx:alpine

## Deploy

```bash
# Build e subir
docker compose up -d --build

# Verificar
curl http://localhost:8180
```

O nginx do host faz reverse proxy para o container na porta 8180.

## Estrutura

```
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── html/
│   └── index.html
└── README.md
```
