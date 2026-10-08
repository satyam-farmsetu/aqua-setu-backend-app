# Package management with uv

We use [uv](https://docs.astral.sh/uv/) to manage Python, the virtual environment and dependencies.

## Why uv

- **One tool** replaces pip, pip-tools, virtualenv and pyenv-style Python installs.
- **Fast**: installs are typically 10–100× faster than pip, which matters for CI and Docker builds.
- **Lockfile**: `uv.lock` pins every package, including transitive dependencies, for all platforms. Everyone and every image installs the same versions.
- **Standard**: dependencies live in `pyproject.toml` under the PEP 621 `[project]` table, so they are not tied to a uv-specific format.

## Alternatives

| Tool | Pros | Cons |
| --- | --- | --- |
| pip + `requirements.txt` | Built in, universal | No lockfile for transitive dependencies (without pip-tools), slow, manual venvs |
| pip-tools | Adds `requirements.lock` to pip | Still slow, separate tools for venv and Python |
| Poetry | Mature, lockfile, popular | Slower. Older versions used a non-standard `[tool.poetry]` dependency format |
| PDM | Standards-based, lockfile | Smaller community |
| Pipenv | Lockfile | Slow, largely superseded |

## How this project is configured

```toml
[tool.uv]
package = false
```

This is an application, not a library, so we never build or install it as a package. Django imports our apps directly from the project root. Because of that there is no `[build-system]` table and no `src/` folder. If we ever need to publish a reusable app, it would get its own package (for example with a uv workspace).

### Extras

Optional dependency groups are defined as extras in `[project.optional-dependencies]`:

- `dev`: tools for developers (see [dependencies.md](dependencies.md))
- `prod`: production-only packages, installed in the prod Docker image

## Common commands

```sh
uv sync --extra dev                 # install everything for local development
uv add django-something             # add a runtime dependency
uv add --optional dev some-tool     # add a dev dependency
uv remove some-tool --optional dev  # remove one
uv lock --upgrade-package django    # upgrade one package
uv lock --upgrade                   # upgrade everything within constraints
uv run <command>                    # run inside .venv without activating it
uv tree                             # show the dependency tree
```

**Gotcha:** `uv add` and `uv remove` re-sync the environment without extras, which uninstalls the dev tools. Run `uv sync --extra dev` afterwards. Moving dev tools from the `dev` extra to a PEP 735 `[dependency-groups]` `dev` group would fix this, because uv installs the `dev` group by default.

## Rules

- Never `pip install` into `.venv`. Use `uv add` so `pyproject.toml` and `uv.lock` stay in sync.
- Commit `uv.lock`. Docker builds use `uv sync --locked`, which fails if the lockfile is out of date.
- Keep version constraints as lower bounds (`>=`). The lockfile provides the exact pins.
