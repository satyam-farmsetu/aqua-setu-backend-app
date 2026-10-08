# Type checking with mypy

```sh
uv run mypy .
```

Config is in [mypy.ini](../mypy.ini). Migrations, tests and build output are excluded.

## Why static typing

- Catches wrong attribute names, `None` handling mistakes and wrong argument types before runtime.
- Type hints make serializers, services and view code easier to read and refactor.
- Editors (Pylance) use the same hints for autocompletion.

## Why mypy

- **Django support**: [django-stubs](https://github.com/typeddjango/django-stubs) ships a mypy plugin (`mypy_django_plugin.main`) that loads our settings and understands model fields, managers, querysets and `AUTH_USER_MODEL`. Other checkers only get the stubs, not the plugin.
- Mature and widely used in the Django ecosystem.

## Stub packages

Many libraries do not ship type information, so we install stubs:

| Stub | For |
| --- | --- |
| `django-stubs` | Django (plus the mypy plugin) |
| `djangorestframework-stubs` | DRF |
| `django-filter-stubs` | django-filter |
| `types-django-import-export` | django-import-export |
| `decouple-types` | python-decouple |

Settings that interact with stubs:

- `cast=Csv()` in `config(...)` needs `# type: ignore` because decouple's types cannot express the cast result.
- If a stub declares an attribute as `list[str]` (for example `REQUIRED_FIELDS`), keep it a list and annotate it with `ClassVar[list[str]]` instead of changing it to a tuple.

## Alternatives

| Checker | Pros | Cons |
| --- | --- | --- |
| **Pyright** / **Pylance** | Very fast, excellent editor integration (Pylance is the VS Code engine) | No Django plugin, so model fields and managers are often typed as `Any` or reported wrongly |
| **basedpyright** | Pyright fork with stricter defaults | Same Django limitation |
| **ty** (Astral) | Very fast, from the makers of Ruff and uv | Young, no Django plugin |
| **Pyre** | Fast | Small ecosystem |

Pylance still runs in VS Code for autocompletion. mypy is the checker that counts for CI.

## Tips

- Annotate function signatures. Local variables are usually inferred.
- Prefer `django-stubs` types such as `QuerySet[User]` over `Any`.
- When a third-party package has no stubs, add an `ignore_missing_imports = True` section for that module in `mypy.ini` rather than ignoring errors everywhere.
