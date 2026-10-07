# Docker setup

How the [Dockerfile](../Dockerfile) and [compose.yaml](../compose.yaml) are built, and why. For commands, see [running-with-docker.md](running-with-docker.md).

## Multi-stage Dockerfile

```
python-base ──┬── uv-base ──┬── dev       (runserver, keeps uv)
              │             └── builder   (uv sync --extra prod → /opt/venv)
              └── prod  ←── COPY /opt/venv from builder
```

| Stage | Based on | Purpose |
| --- | --- | --- |
| `python-base` | `python:3.14-slim` | Shared env vars (`PYTHONUNBUFFERED`, venv on `PATH`) and `WORKDIR` |
| `uv-base` | `python-base` | Adds the uv binary (copied from `ghcr.io/astral-sh/uv`) |
| `dev` | `uv-base` | Runtime deps + uv, for Compose. Code is bind-mounted |
| `builder` | `uv-base` | Installs runtime + `prod` deps into `/opt/venv`, compiles bytecode |
| `prod` | `python-base` | Copies only `/opt/venv` and the code. No uv, no build cache |

Build a stage with `--target`:

```sh
docker build --target prod -t aqua-setu-backend:prod .
```

### Why multi-stage

- **Smaller, safer prod image**: build tools (uv) and caches stay in the builder stage, so they are not shipped and cannot be exploited.
- **One file for dev and prod**: both use the same base image and lockfile, so they cannot drift apart.
- **Fast rebuilds**: dependencies are installed in their own layer before `COPY . .`. Changing code does not reinstall dependencies.

## Practices used in the Dockerfile

| Practice | Where | Why |
| --- | --- | --- |
| Slim base image | `python:3.14-slim` | Small, but glibc-based, so wheels (psycopg-binary) just work. Alpine uses musl and often needs compilation |
| Pinned uv minor version | `uv:0.12` | Reproducible builds |
| `uv sync --locked` | builder, dev | Fails if `uv.lock` is out of date instead of silently resolving new versions |
| Bind-mount `pyproject.toml` and `uv.lock` for the install step | `RUN --mount=type=bind` | Dependency layer only rebuilds when these files change |
| uv cache mount | `--mount=type=cache` | Downloads are reused across builds but not stored in the image |
| `UV_LINK_MODE=copy` | uv-base | Required because the cache is on a different mount |
| `UV_COMPILE_BYTECODE=1` | builder | Precompiled `.pyc` files mean faster container start-up |
| `UV_PYTHON_DOWNLOADS=0` | uv-base | Always use the image's Python, never download one |
| venv at `/opt/venv` | everywhere | The dev bind mount of `.:/app` does not hide it, and `prod` can copy it as one directory |
| Non-root user | prod | Limits damage if the app is compromised |
| `collectstatic` at build time | prod | Static files are part of the immutable image, served by WhiteNoise |
| `.dockerignore` | repo root | Keeps `.env`, `.git`, `.venv` and caches out of the build context and the image |
| Exec-form `CMD [...]` | dev, prod | Signals reach the process, so containers stop cleanly |

`collectstatic` imports settings, which require `SECRET_KEY` and `POSTGRES_*`. The prod stage passes placeholder values for that one command only. Real values come from the environment at runtime.

## Compose

- `db`: `postgres:18-alpine` with a `pg_isready` health check and a named volume (`postgres_data`). Postgres 18 images expect the volume at `/var/lib/postgresql`.
- `backend`: the `dev` stage. It waits for `db` to be healthy, runs `migrate`, then `runserver`. `.:/app` is bind-mounted for live reload.

Compose reads `.env` both for `${...}` substitution and for the backend's environment, so `.env` is the single source of configuration.

## Alternatives considered

| Instead of | Alternative | Why not (for now) |
| --- | --- | --- |
| Multi-stage | Single-stage image | Ships uv and caches, so the image is bigger and has a larger attack surface |
| `python:*-slim` | Alpine | musl breaks many binary wheels, so builds need compilers and are slower |
| `python:*-slim` | Distroless or Chainguard | Even smaller, but no shell, which makes debugging harder. Worth revisiting for prod |
| Bind mount | `docker compose watch` | Bind mounts are simpler and work on every platform |
| Migrate in prod `CMD` | Separate migrate step | Several replicas would race to migrate at the same time. Run it once per deploy |
