# project-name

- **Author**: Fernando Neira-Roman
- **Status**: draft
- **Date**: YYYY-MM-DD

One-paragraph description of the project: goal, inputs, main outputs.

## Structure

```
.
├── config/
│   └── config.yml        # SSOT for paths and constants (read-only)
├── data/                 # NOT versioned (only .gitkeep)
│   ├── raw/              # Original, immutable input data
│   ├── interim/          # Intermediate transformations
│   ├── processed/        # Final, analysis-ready data
│   └── external/         # Third-party data
├── documents/
│   ├── plans/            # Versioned: implementation plans, decision logs
│   ├── references/       # NOT versioned: papers, ebooks (third-party)
│   └── status/           # Versioned: stage status notes
├── models/               # NOT versioned — trained models
├── outputs/              # NOT versioned — generated results
│   ├── figures/
│   ├── tables/
│   └── reports/          # Rendered reports
├── src/
│   ├── functions/        # One function per file (file name = function name)
│   ├── reports/          # Report sources (.qmd / .Rmd), created when needed
│   └── main.R | main.py  # Thin orchestrator (copy from templates/)
├── templates/            # Starting points for new scripts; symlink_example.md
├── .env.example          # Secret keys to fill in `.env` (never versioned)
├── .gitignore
├── LICENSE               # PolyForm Noncommercial 1.0.0
├── .lintr                # R linter configuration
├── .python-version       # Python version (3.12)
├── air.toml              # R formatter configuration
├── pyproject.toml        # Python dependencies and tool configuration
└── uv.lock               # Locked Python environment (versioned)
```

## Getting started

1. Create the repository from this template:
   `gh repo create <project-name> --template <your-github-user>/<template-repo> --private --clone`
   (or the **Use this template** button on GitHub).
2. Rename the title of this README and fill in the metadata block.
3. `cp .env.example .env` and fill in the secrets.
4. Copy `templates/main_template.R` (or `.py`) to `src/main.R` (or `.py`).
5. For each new function, copy `templates/function_template.*` to
   `src/functions/<function_name>.*`.
6. The orchestrator reads `config/config.yml` itself. When a second script needs the
   config, copy `templates/load_config.*` to `src/functions/` and call `load_config()`.

Run everything from the project root: `Rscript src/main.R` or
`uv run python src/main.py`.

Large or shared datasets stay outside the project. Link them into `data/` with a symbolic
link instead of copying; see `templates/symlink_example.md` for Linux, macOS and Windows.

Check style before committing (same result in any editor):

```sh
air format .                        # R formatting
Rscript -e 'lintr::lint_dir()'      # R lint
uv run ruff check . && uv run black .   # Python lint + formatting
```

## Dependencies

- **Python:** `uv add <package>` (pinned in `uv.lock`).
- **R:** install the packages the templates need, `install.packages(c("yaml", "purrr", "readr"))`.
  Add other packages per project. To lock R packages for a project, opt in with `renv::init()`.

## Reports

Write report sources (.qmd / .Rmd) in `src/reports/` (create it when needed; versioned).
Rendered output goes to `outputs/reports/` (not versioned).

## Tests

Tests are not part of the template. If a project needs them, put them in `tests/`.

## Conventions

Single source for the project's style rules. Enforced by `.lintr`, `air.toml` and `pyproject.toml`.

| Element | Convention | Example |
|---|---|---|
| Folders | full lowercase words; kebab-case if multi-word | `outputs/figures/` |
| Function files | `lower_snake_case`, one function per file | `compute_importance.R` |
| Functions | `lower_snake_case`, verb first | `compute_importance()` |
| Local variables | language style guide (`snake_case`) | `station_count` |
| Global variables / constants / config keys | `SCREAMING_SNAKE_CASE` | `PATH_DATA_RAW`, `CRS_OUTPUT` |
| kebab-case | reserved for multi-word folders and special cases (repo names, CLI flags, URLs) | `decision-logs/`, `climate-interpolation` |

- Code, comments and documentation in English.
- R: Google R Style Guide (tidyverse fallback), `<-`, `|>`, explicit `return()`,
  roxygen header on every script, 80 columns.
- Python: Google Python Style Guide (PEP 8 fallback), type hints and Google docstrings,
  Black formatting and Ruff lint, 88 columns.
- Paths and constants come only from `config/config.yml`; secrets only from `.env`.
- Functions are pure; I/O happens in the orchestrator.

## License

Copyright 2026 Fernando Neira-Roman. Free to use, copy and modify for non-commercial purposes
under the PolyForm Noncommercial License 1.0.0 (see `LICENSE`). Commercial use requires written
permission from the author. Copies must keep the notice and the license terms.

Projects that belong to a client or employer replace `LICENSE` with the terms they agree on.
