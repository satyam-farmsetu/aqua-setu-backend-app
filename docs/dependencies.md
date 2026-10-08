# Dependencies

What every dependency in [pyproject.toml](../pyproject.toml) does, why we chose it, and what could replace it.

Dependencies are split into three groups:

| Group | Installed by | Purpose |
| --- | --- | --- |
| `dependencies` | always | Needed to run the app anywhere |
| `prod` extra | `uv sync --extra prod`, prod Docker image | Serving and storage in deployed environments |
| `dev` extra | `uv sync --extra dev` | Linting, typing, testing on developer machines |

## Runtime

| Package | What it does | Why we use it | Alternatives |
| --- | --- | --- | --- |
| **django** | Web framework: ORM, migrations, admin, auth | Mature, batteries included, strong admin for operations staff | FastAPI + SQLAlchemy (faster async APIs, but no admin or migrations out of the box), Flask, Litestar |
| **djangorestframework** (DRF) | Serializers, viewsets, permissions, browsable API | The standard for REST on Django, with a huge ecosystem | Django Ninja (Pydantic-based, typed, faster to write), plain Django views |
| **djangorestframework-simplejwt** | JWT access and refresh tokens | Stateless auth for mobile and SPA clients. We enable refresh rotation and blacklisting (`token_blacklist`) | django-rest-knox (DB-backed tokens, easy to revoke), DRF `TokenAuthentication` (simple, one token per user), dj-rest-auth or django-allauth (full signup, login and social flows) |
| **drf-spectacular** `[sidecar]` | Generates an OpenAPI 3 schema, Swagger UI and ReDoc | Actively maintained, OpenAPI 3. `sidecar` serves the UI assets locally instead of from a CDN | drf-yasg (OpenAPI 2 only, effectively in maintenance mode) |
| **django-filter** | Declarative `?field=value` filtering for querysets | Plugs into DRF via `DjangoFilterBackend` | Hand-written `get_queryset` filtering, DRF `SearchFilter`/`OrderingFilter` only |
| **django-cors-headers** | Sends CORS headers | Lets browser front ends on another origin call the API | Configure CORS in the reverse proxy (nginx, Caddy) |
| **django-import-export** | CSV/Excel import and export in the admin | Bulk data entry by operations staff without custom code | Custom management commands, pandas scripts |
| **django-redis** | Redis cache backend | Rich Redis features (raw client access, compression, locks) | Django's built-in `django.core.cache.backends.redis.RedisCache` (enough for basic caching), Memcached |
| **django-extensions** | `shell_plus`, `graph_models`, `show_urls`, and more | Developer productivity | IPython plus individual scripts |
| **python-decouple** | Reads settings from environment variables and `.env` | Small, with a simple `config("KEY", cast=...)` API | django-environ (also parses `DATABASE_URL`), pydantic-settings (typed and validated settings) |
| **psycopg** `[binary]` | PostgreSQL driver (psycopg 3) | Modern driver with async support. `binary` ships prebuilt wheels, so no compiler or libpq is needed | `psycopg[c]` (compiled against the system libpq, recommended by psycopg for production), psycopg2 (legacy) |

> `django-redis` is installed but no cache is configured yet, and Compose does not run Redis. Add both when caching is needed.

## Production (`prod` extra)

| Package | What it does | Why we use it | Alternatives |
| --- | --- | --- | --- |
| **gunicorn** | WSGI application server | Battle-tested, simple process model | uWSGI (more knobs, harder to configure), Granian (Rust, fast), uvicorn or gunicorn + uvicorn workers (if we move to ASGI/async views) |
| **whitenoise** | Serves static files (admin, Swagger UI) from the app | No separate nginx needed for static assets. Adds compression and cache-busting filenames | nginx or Caddy in front of the app, CDN or S3 for static files |
| **django-storages** `[s3]` | Stores uploaded media in S3-compatible storage | Our media goes to Supabase Storage through its S3-compatible API. Containers have no persistent disk | Local disk with a volume (single server only), django-storages backends for GCS or Azure |

Static files (from `collectstatic`) and media (user uploads) are handled separately on purpose. Static files are built into the image, while media must outlive containers.

## Development (`dev` extra)

| Package | What it does | Alternatives / notes |
| --- | --- | --- |
| **ruff** | Linter, import sorter and formatter | See [linting-and-formatting.md](linting-and-formatting.md) |
| **mypy** | Static type checker | See [type-checking.md](type-checking.md) |
| **django-stubs**, **djangorestframework-stubs**, **django-filter-stubs**, **types-django-import-export**, **decouple-types** | Type information for libraries that do not ship their own | Required for mypy to understand Django and DRF. See [type-checking.md](type-checking.md) |
| **coverage** | Measures which lines the tests run | pytest + pytest-cov (if we switch from Django's test runner to pytest) |
| **pygraphviz** | Renders `graph_models` diagrams | `graph_models` can also output `.dot` files with no extra dependency. Needs Graphviz system headers to install |

## Rules of thumb

- Add a package to `dependencies` only if production code imports it. Everything else goes in an extra.
- Prefer packages that are actively maintained and support the current Django and Python versions.
- Always commit `uv.lock` together with `pyproject.toml`.
- When adding a dependency, add a row to this file.
