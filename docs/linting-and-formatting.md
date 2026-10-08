# Linting and formatting: Ruff

We use **Ruff** as the only linter and formatter. Together with [mypy](type-checking.md), it covers everything we used to run Pylint for.

```sh
uv run ruff check --fix .    # lint, auto-fix, sort imports
uv run ruff format .         # format
```

## Ruff

[Ruff](https://docs.astral.sh/ruff/) is a linter and formatter written in Rust. It re-implements the rules of Flake8, isort, pyupgrade, Pylint, pydocstyle, Black and many plugins in one tool.

**Why**

- **Speed**: it checks the whole project in milliseconds, so it runs on every save in the editor.
- **One tool, one config** (`[tool.ruff]` in `pyproject.toml`) instead of Black + isort + Flake8 + Pylint + plugins.
- **Auto-fix**: many rules fix themselves (`--fix`), for example sorting imports or modernising syntax.
- The formatter output is compatible with Black's.

**Rules we enable** (`[tool.ruff.lint] select`):

| Code     | Source                      | Catches                                                                      |
| -------- | --------------------------- | ---------------------------------------------------------------------------- |
| `E`, `W` | pycodestyle                 | Style errors                                                                 |
| `F`      | Pyflakes                    | Unused imports and variables, undefined names                                |
| `I`      | isort                       | Import order                                                                 |
| `N`      | pep8-naming                 | Naming conventions (`snake_case`, `CapWords`, `UPPER_CASE`)                  |
| `D1`     | pydocstyle                  | Missing docstrings on modules, packages, classes, functions and methods      |
| `B`      | flake8-bugbear              | Likely bugs, such as mutable default arguments                               |
| `UP`     | pyupgrade                   | Outdated syntax for our Python version                                       |
| `SIM`    | flake8-simplify             | Code that can be simpler                                                     |
| `DJ`     | flake8-django               | Django pitfalls, such as `null=True` on string fields or a missing `__str__` |
| `PL`     | Pylint rules ported to Ruff | Design limits (too many arguments or branches), comparisons, misc. checks    |
| `RUF`    | Ruff's own rules            | For example `RUF012`: mutable class attributes                               |

`E501` (line too long) is ignored because the formatter handles line length.

Docstrings are required everywhere: every module, package (`__init__.py`), public class, function and method, including magic methods and `__init__`. A one-line docstring that says what the file or object is for is enough.

Migrations are excluded.

**Example: RUF012.** `fields = [...]` in a serializer's `Meta` is a mutable class attribute. Use a tuple instead: `fields = (...)`. Where a library's type stubs require a list, annotate it: `REQUIRED_FIELDS: ClassVar[list[str]] = [...]`.

## Why not Pylint

We used Pylint with `pylint-django` earlier and dropped it, because Ruff and mypy cover what it did:

| What Pylint gave us                                                  | Now covered by                      |
| -------------------------------------------------------------------- | ----------------------------------- |
| Cross-module checks (missing methods, wrong arguments)               | mypy, which is more precise         |
| Understanding Django models, managers and settings (`pylint-django`) | mypy's django-stubs plugin          |
| Pylint rules (too many arguments or branches, and so on)             | Ruff `PL`                           |
| Missing docstrings                                                   | Ruff `D1`                           |
| Naming conventions                                                   | Ruff `N`                            |
| Unused imports and variables                                         | Ruff `F`                            |

Pylint was also much slower (seconds rather than milliseconds), needed its own config file, and raised false positives. For example, it flagged `INSTALLED_APPS` as a bad variable name once the setting was extended with `+=`.

The one thing it did that nothing here replaces is duplicate-code detection. If that becomes a need, run `pylint --disable=all --enable=duplicate-code` occasionally, or use a dedicated tool.

## What Ruff replaced

| Tool                   | Replaced by                                 |
| ---------------------- | ------------------------------------------- |
| Black                  | `ruff format`                               |
| isort                  | Ruff `I` rules                              |
| Flake8 + plugins       | Ruff rules (`E`, `W`, `F`, `B`, `SIM`, ...) |
| pyupgrade              | Ruff `UP` rules                             |
| Pylint + pylint-django | Ruff `PL`, `N`, `D1` + mypy                 |

## Editor

`.vscode/settings.json` sets Ruff (`charliermarsh.ruff`) as the Python formatter and runs fix-all and organise-imports on save. Install the recommended extensions from `.vscode/extensions.json`.

## Suppressing a warning

Fix the code if you can. If not, suppress the warning on one line and explain why:

```python
from django.core.management import execute_from_command_line  # noqa: PLC0415  (lazy import is intentional)
```

Use `per-file-ignores` in `pyproject.toml` for whole files (for example `manage.py`). Avoid disabling rules globally.
