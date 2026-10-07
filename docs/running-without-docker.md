# Running without Docker

Run Django directly on your machine with `uv`. You still need a PostgreSQL server. The easiest option is to start only the database container, but a locally installed Postgres works too.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Python 3.14. uv reads `.python-version`; if you use pyenv, `pyenv install 3.14` is enough. Otherwise `uv python install 3.14`.
- PostgreSQL (any recent version; Docker uses 18)
- Graphviz headers, required to build `pygraphviz` (a dev dependency):
  - Debian/Ubuntu: `sudo apt install graphviz libgraphviz-dev`
  - macOS: `brew install graphviz`

## Setup

```sh
cp .env.example .env
uv sync --extra dev
```

`uv sync` creates `.venv/` and installs exactly what is in `uv.lock`. `--extra dev` adds linters, type stubs and coverage.

> If a shell from another project has `VIRTUAL_ENV` set, uv warns and ignores it. Run `deactivate` or open a new shell to silence the warning.

## Database

Choose one.

**Option A: Postgres in Docker, Django on your host**

```sh
docker compose up -d db
```

The values in `.env.example` (`localhost:5432`, user and password `postgres`, database `aqua_setu`) already match.

**Option B: local Postgres**

Create a user and a database, then set `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST` and `POSTGRES_PORT` in `.env`:

```sh
sudo -u postgres createuser --createdb --pwprompt aqua_setu
sudo -u postgres createdb --owner aqua_setu aqua_setu
```

The user needs `CREATEDB` because Django creates a `test_*` database when it runs tests.

## Run

```sh
uv run manage.py migrate
uv run manage.py createsuperuser
uv run manage.py runserver
```

Open http://localhost:8000/schema/swagger-ui/.

`uv run` uses `.venv` without you having to activate it. You can also `source .venv/bin/activate` and call `python manage.py ...`.

## Tests

```sh
uv run manage.py test
```

With coverage:

```sh
uv run coverage run manage.py test
uv run coverage report      # or: uv run coverage html
```

## Code quality

Run these before pushing:

```sh
uv run ruff check --fix .    # lint + sort imports
uv run ruff format .         # format
uv run pylint **/*.py        # Django-aware lint
uv run mypy .                # type check
```

VS Code applies Ruff on save if you install the recommended extensions (`.vscode/extensions.json`).

## Adding or removing dependencies

```sh
uv add <package>                    # runtime
uv add --optional dev <package>     # dev only
uv add --optional prod <package>    # production only
uv sync --extra dev                 # re-install dev tools afterwards
```

`uv add` and `uv remove` re-sync without extras, which uninstalls the dev tools. That is why `uv sync --extra dev` is needed afterwards. See [package-management.md](package-management.md).

## Model diagram

`django-extensions` and `pygraphviz` can draw the models:

```sh
uv run manage.py graph_models -a -o models.png
```
