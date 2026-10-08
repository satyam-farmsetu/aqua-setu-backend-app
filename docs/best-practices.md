# Project conventions and best practices

## Configuration

- **All configuration comes from environment variables**, read with `python-decouple`'s `config()` in `aqua_setu/settings.py`. Locally they come from `.env`, and in deployed environments from the platform's environment.
- `.env` is git-ignored. `.env.example` is committed and lists every variable with safe local defaults. When you add a setting, add it to `.env.example` too.
- `ENV` (`dev` or anything else) switches environment-specific behaviour: the insecure default `SECRET_KEY`, `DEBUG`, WhiteNoise, S3 storage and the browsable API. Outside `dev`, a missing secret makes the app fail at start-up on purpose.
- One settings file with `ENV` switches, rather than `settings/dev.py` and `settings/prod.py`, so that the differences stay small and visible.

## Database

- PostgreSQL everywhere, including dev and tests, so we never ship SQL that only worked on SQLite.
- Commit every migration. Name non-trivial ones: `makemigrations accounts --name add_phone_number`.
- Never edit a migration that has already been applied in a shared environment. Write a new one.

## Apps and code layout

- One Django app per business area (`accounts`, ...). Create new ones with `uv run manage.py startapp <name>` and register them under "Local apps" in `INSTALLED_APPS`.
- Inside an app, use packages rather than single large files, as `accounts` does:

  ```
  accounts/
    admin/  managers/  models/  serializers/  views/  urls/  utils/  tests/
  ```

  Re-export public classes from each package's `__init__.py`.
- Use a custom user model from the start (`AUTH_USER_MODEL = "accounts.User"`, email as the login field). Always refer to it with `get_user_model()` or `settings.AUTH_USER_MODEL`, never with `django.contrib.auth.models.User`.

## API

- **Versioned URLs**: everything lives under `/v1/`. Breaking changes go into `/v2/` while `/v1/` keeps working.
- Defaults (in `REST_FRAMEWORK`): JWT auth, `IsAuthenticated`, limit/offset pagination (100), search, ordering and django-filter backends. Open an endpoint up deliberately with `permission_classes = (AllowAny,)`.
- Document endpoints with `@extend_schema` so the Swagger UI stays accurate.
- Restrict methods with `http_method_names` on viewsets that should not allow writes.
- In serializer `Meta`, use tuples for `fields` and `read_only_fields` (Ruff `RUF012`).

## Code quality

Before pushing:

```sh
uv run ruff check --fix . && uv run ruff format . && uv run mypy . && uv run manage.py test
```

- Type-annotate function signatures. mypy must pass.
- Every module, package, class, function and method needs a docstring (Ruff `D1`). One line is enough.
- Keep Ruff clean rather than accumulating `# noqa`. When a suppression is justified, scope it to one line and give the reason.
- Write tests in `<app>/tests/` using Django's test runner (`TestCase`, `APITestCase`).

## Dependencies

- Use `uv add`, never `pip install`. Commit `uv.lock`.
- Runtime, `prod` and `dev` dependencies are kept separate. See [dependencies.md](dependencies.md).
- Document new dependencies in [dependencies.md](dependencies.md).

## Security

- Never commit secrets. Rotate any that leak.
- `DEBUG` is off outside `dev`, and the browsable API is disabled there.
- Set `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS` explicitly per environment.
- JWT refresh tokens rotate and old ones are blacklisted.
- The prod container runs as a non-root user.
