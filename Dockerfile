# syntax=docker/dockerfile:1

# ---------------------------------------------------------------------------
# python-base: shared runtime settings for every stage
# ---------------------------------------------------------------------------
FROM python:3.14-slim AS python-base

# Keep the venv outside /app so the dev bind mount doesn't hide it
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app


# ---------------------------------------------------------------------------
# uv-base: python-base + uv, used to install dependencies
# ---------------------------------------------------------------------------
FROM python-base AS uv-base

COPY --from=ghcr.io/astral-sh/uv:0.12 /uv /uvx /bin/

ENV UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_PYTHON_DOWNLOADS=0


# ---------------------------------------------------------------------------
# dev: base dependencies + uv, source code is bind-mounted by compose.yaml
# ---------------------------------------------------------------------------
FROM uv-base AS dev

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# ---------------------------------------------------------------------------
# builder: install production dependencies into /opt/venv
# ---------------------------------------------------------------------------
FROM uv-base AS builder

ENV UV_COMPILE_BYTECODE=1

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --extra prod


# ---------------------------------------------------------------------------
# prod: slim runtime image with only the venv and app code (no uv)
# ---------------------------------------------------------------------------
FROM python-base AS prod

RUN useradd --system --uid 1000 --no-create-home app

COPY --from=builder /opt/venv /opt/venv
COPY . .

# Settings require these at import time; placeholder values are only used to collect static files
RUN ENV=prod SECRET_KEY=collectstatic \
    POSTGRES_DB=_ POSTGRES_USER=_ POSTGRES_PASSWORD=_ POSTGRES_HOST=_ \
    python manage.py collectstatic --noinput

USER app

EXPOSE 8000

CMD ["gunicorn", "aqua_setu.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
