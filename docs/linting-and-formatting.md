# Linting and formatting: Ruff and Pylint

We use **Ruff** as the main linter and the only formatter, and **Pylint** with `pylint-django` as a second, slower, deeper check.

```sh
uv run ruff check --fix .    # lint, auto-fix, sort imports
uv run ruff format .         # format
uv run pylint **/*.py        # Django-aware lint
```

## Ruff

[Ruff](https://docs.astral.sh/ruff/) is a linter and formatter written in Rust. It re-implements the rules of Flake8, isort, pyupgrade, Black and many plugins in one tool.

**Why**

- **Speed**: it checks the whole project in milliseconds, so it runs on every save in the editor.
- **One tool, one config** (`[tool.ruff]` in `pyproject.toml`) instead of Black + isort + Flake8 + plugins.
- **Auto-fix**: many rules fix themselves (`--fix`), for example sorting imports or modernising syntax.
- The formatter output is compatible with Black's.

**Rules we enable** (`[tool.ruff.lint] select`):

| Code | Source | Catches |
| --- | --- | --- |
| `E`, `W` | pycodestyle | Style errors |
| `F` | Pyflakes | Unused imports and variables, undefined names |
| `I` | isort | Import order |
| `B` | flake8-bugbear | Likely bugs, such as mutable default arguments |
| `UP` | pyupgrade | Outdated syntax for our Python version |
| `SIM` | flake8-simplify | Code that can be simpler |
| `DJ` | flake8-django | Django pitfalls, such as `null=True` on string fields or a missing `__str__` |
| `PL` | Pylint rules ported to Ruff | A subset of Pylint checks |
| `RUF` | Ruff's own rules | For example `RUF012`: mutable class attributes |

`E501` (line too long) is ignored because the formatter handles line length. Migrations are excluded.

**Example: RUF012.** `fields = [...]` in a serializer's `Meta` is a mutable class attribute. Use a tuple instead: `fields = (...)`. Where a library's type stubs require a list, annotate it: `REQUIRED_FIELDS: ClassVar[list[str]] = [...]`.

## Pylint

[Pylint](https://pylint.readthedocs.io/) is the oldest and most thorough Python linter. With the `pylint-django` plugin it loads the Django settings (`django-settings-module` in `.pylintrc`) and understands models, managers and querysets.

**Why we still keep it next to Ruff**

- Ruff checks one file at a time. Pylint infers types across modules, so it finds things Ruff cannot: calling a method that does not exist, wrong argument counts, or misuse of a model field.
- `pylint-django` removes Django false positives (for example `objects` "not existing" on models) and adds Django-specific checks.
- Some Pylint checks, such as design limits, duplicate code and missing docstrings, have no Ruff equivalent yet.

**Cost**: it is much slower (seconds rather than milliseconds) and noisier, so it runs before pushing or in CI, not on every keystroke.

Config lives in [.pylintrc](../.pylintrc).

## Ruff vs Pylint at a glance

| | Ruff | Pylint |
| --- | --- | --- |
| Speed | Very fast (Rust) | Slow (Python, type inference) |
| Formatter | Yes | No |
| Auto-fix | Many rules | No |
| Cross-module inference | No | Yes |
| Django awareness | `DJ` rules (simple patterns) | `pylint-django` (loads settings and models) |
| Config | `pyproject.toml` | `.pylintrc` |
| Best for | Every save, pre-commit | CI and pre-push |

If Pylint ever becomes more noise than value, it is safe to drop it, along with `pylint-django` and `.pylintrc`, and rely on Ruff + mypy. Most of its high-value checks are covered by Ruff's `PL` rules or by mypy.

## What Ruff replaced

| Tool | Replaced by |
| --- | --- |
| Black | `ruff format` |
| isort | Ruff `I` rules |
| Flake8 + plugins | Ruff rules (`E`, `W`, `F`, `B`, `SIM`, ...) |
| pyupgrade | Ruff `UP` rules |

## Editor

`.vscode/settings.json` sets Ruff (`charliermarsh.ruff`) as the Python formatter and runs fix-all and organise-imports on save. Install the recommended extensions from `.vscode/extensions.json`.

## Suppressing a warning

Fix the code if you can. If not, suppress the warning on one line and explain why:

```python
from django.core.management import execute_from_command_line  # noqa: PLC0415  (lazy import is intentional)
```

Use `per-file-ignores` in `pyproject.toml` for whole files (for example `manage.py`). Avoid disabling rules globally.
