# Running with Docker

This is the recommended setup. It runs PostgreSQL and the Django dev server in containers, so the only thing you need installed is Docker.

## Prerequisites

- Docker Engine or Docker Desktop, with Compose v2 (`docker compose version`)

## First run

```sh
cp .env.example .env
docker compose up --build
```

This will:

1. Build the `dev` stage of the [Dockerfile](../Dockerfile).
2. Start Postgres 18 and wait until its health check passes.
3. Run `python manage.py migrate`.
4. Start `runserver` on http://localhost:8000.

Your source code is bind-mounted into the container, so code changes reload automatically. There is no need to rebuild.

Create an admin user (in another terminal):

```sh
docker compose exec backend python manage.py createsuperuser
```

## How the configuration works

- The `POSTGRES_*` values in `.env` are used by **both** services: the `db` container creates the database and user from them, and Django connects with them.
- Inside Compose, `POSTGRES_HOST` is overridden to `db` (the service name). The `localhost` value in `.env` is for [running without Docker](running-without-docker.md).
- Postgres is also published on `localhost:${POSTGRES_PORT}` (default 5432), so you can connect with a GUI client or run Django on your host against it.

## Everyday commands

| Task | Command |
| --- | --- |
| Start (in background) | `docker compose up -d` |
| Follow logs | `docker compose logs -f backend` |
| Stop | `docker compose down` |
| Make migrations | `docker compose exec backend python manage.py makemigrations` |
| Apply migrations | `docker compose exec backend python manage.py migrate` |
| Django shell | `docker compose exec backend python manage.py shell_plus` |
| Run tests | `docker compose exec backend python manage.py test` |
| psql | `docker compose exec db psql -U postgres -d aqua_setu` |

Files that `makemigrations` creates appear on your host because of the bind mount.

## When to rebuild

Dependencies are installed into the image at `/opt/venv`, not into the mounted folder. After changing `pyproject.toml` or `uv.lock`, rebuild:

```sh
docker compose up --build
```

## Resetting the database

The data lives in the `postgres_data` named volume. To wipe it:

```sh
docker compose down -v
```

## Linters and type checking

The dev image only contains runtime dependencies. Run Ruff, Pylint and mypy on your host with `uv` (see [running without Docker](running-without-docker.md#code-quality)). They do not need the database.

## Building the production image

```sh
docker build --target prod -t aqua-setu-backend:prod .
docker run --rm -p 8000:8000 --env-file .env.prod aqua-setu-backend:prod
```

The prod image runs gunicorn as a non-root user and does **not** run migrations. Run `python manage.py migrate` as a separate step when deploying. See [docker.md](docker.md) for how the image is structured.

## Troubleshooting

- **`Cannot connect to the Docker daemon`**: start Docker Desktop or the Docker service.
- **Port 5432 or 8000 already in use**: stop the local Postgres or server, or change `POSTGRES_PORT` in `.env` (this only changes the host-side port).
- **`password authentication failed`** after changing `POSTGRES_*`: Postgres only reads these values the first time the volume is created. Run `docker compose down -v` to recreate it.
