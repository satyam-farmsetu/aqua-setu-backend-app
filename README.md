# AquaSetu Backend

REST API for AquaSetu, built with Django 6.1 and Django REST Framework on Python 3.14 and PostgreSQL.

## Quick start

```sh
cp .env.example .env
docker compose up --build
```

The API is then at http://localhost:8000 and the Swagger UI at http://localhost:8000/schema/swagger-ui/.

## Documentation

All documentation is in the [docs/](docs/) folder.

### Running the project

| Doc | What it covers |
| --- | --- |
| [Running with Docker](docs/running-with-docker.md) | Recommended setup: Postgres and the API in containers, everyday commands, troubleshooting |
| [Running without Docker](docs/running-without-docker.md) | Local Python with `uv`, Postgres installed locally or in a container, tests, code-quality commands |

### Tooling and decisions

Each page explains what we use, why, and what the alternatives are.

| Doc | What it covers |
| --- | --- |
| [Dependencies](docs/dependencies.md) | Every package in `pyproject.toml`: purpose, reason, alternatives |
| [Package management](docs/package-management.md) | uv vs pip, Poetry and others; lockfile; extras; common commands |
| [Linting and formatting](docs/linting-and-formatting.md) | Ruff: enabled rules, why not Pylint, what it replaced |
| [Type checking](docs/type-checking.md) | mypy vs Pyright and others; Django type stubs |
| [Docker](docs/docker.md) | Multi-stage Dockerfile and Compose, practices used |
| [Best practices](docs/best-practices.md) | Project conventions: config, database, app layout, API, security |

## Project layout

```
aqua_setu/        Django project: settings, root URLs, WSGI/ASGI
accounts/         App: custom User model (email login), /v1/accounts/ endpoints
docs/             Documentation
Dockerfile        Multi-stage image (dev, prod)
compose.yaml      Local Postgres + backend
pyproject.toml    Dependencies and tool config (Ruff)
mypy.ini          mypy config
```

## Useful URLs

| URL | What |
| --- | --- |
| `/admin/` | Django admin |
| `/schema/swagger-ui/` | Swagger UI |
| `/schema/redoc/` | ReDoc |
| `/schema/` | Raw OpenAPI schema |
| `/v1/...` | Version 1 of the API |
