# Cesium secrets

A web service for creating and retrieving secret messages using a secret key and hash.

## Stack

- **Python 3.14**, **uv**
- **FastAPI** + SQLAlchemy (PostgreSQL)
- **Hypercorn** — ASGI server
- **Docker Compose** — orchestration

## How it works

1. Create a secret message with a secret key — you get a unique hash.
2. Retrieve the message later using the hash and the same secret key.
3. Messages are stored encrypted on disk; metadata is kept in PostgreSQL.

## Limits

- Max message size: **50 KB** (configurable via `max_message_size`)
- Max total storage: **2 GB** (configurable via `max_storage_bytes`) — oldest messages are evicted when the limit is reached

## Quick start

```bash
cp backend/.env.template backend/.env
make dev
```

## Deployment

The service is deployed on a VPS behind [Traefik](https://traefik.io/) reverse proxy with automatic HTTPS (Let's Encrypt) at [secrets.csmmark.me](https://secrets.csmmark.me).

Shares PostgreSQL with [UrlShortener](https://github.com/MarkCesium/UrlShortener) (separate database in the same instance).

**CI/CD:** GitHub Actions — push to `master` triggers deploy via SSH (`docker compose up -d --build`).

**Required GitHub Secrets:** `HOST`, `USERNAME`, `PRIVATE_KEY`.

## Project structure

```
├── docker-compose.yaml            # base service definition
├── docker-compose.dev.yaml        # dev overrides (local Postgres, ports)
├── docker-compose.prod.yaml       # prod overrides (Traefik, shared network)
├── Makefile                       # dev, prod, down, logs
│
└── backend/
    ├── src/
    │   ├── main.py                # FastAPI app, middleware, exception handler
    │   ├── api/
    │   │   ├── dao.py             # data access (create, get, eviction)
    │   │   └── views.py           # route handlers
    │   ├── core/
    │   │   ├── config.py          # pydantic-settings configuration
    │   │   ├── db.py              # async SQLAlchemy engine & session
    │   │   └── models/            # Message ORM model
    │   └── utils/
    │       ├── files.py           # async file I/O
    │       ├── flashes.py         # session-based flash messages
    │       └── hasher.py          # SHA256 hashing
    ├── templates/                 # Jinja2 HTML templates
    ├── migrations/                # Alembic migrations
    └── Dockerfile
```
