# Unify FOLDER_TEMPLATE (local) and template-folders-structure (remote) into one R + Python spatial template

- **Date**: 2026-10-26 22:05 (last amended 2026-10-27)
- **Request**: Unify two folder-structure templates for spatial analysis and environmental modelling (R + Python), keeping what is useful from each.
- **Target root**: /Users/fneira/Documents/GITHUB/FOLDER_TEMPLATE
- **Final version**: v2, amended after execution (see "Amendment 2026-10-27")
- **Critical findings**: v1 2 → v2 1 (text fixed, not re-verified) → after amendment: see "Pre-mortem"
- **Approval**: "ejecuta el plan" received 2026-10-27 (00:51 -03). Steps 0–13 were executed under the original authorization, confirmed by the user on 2026-10-27.
- **Status**: executed

> **Agreed scope (binding):** nothing is published to GitHub. The remote `fneira-ciren-code/template-folders-structure` belongs to another account; the user will publish manually. Steps 14 and 15 of the original plan (clone, `rsync --delete` to the remote, branch, PR, `isTemplate`) are therefore **excluded**. The remote is used as a read-only reference.

> **Do not re-run.** Steps 1, 2, 3 and 11a are not idempotent. This plan is a record of what was done and the current design. To change the template, write a new plan.

---

## Final plan

### Amendment 2026-10-27 (after execution, at the user's request)
- `reports/` at the root was removed, and so was `PATH_REPORTS`. Report sources go in `src/reports/` (created when needed, versioned). Rendered output goes in `outputs/reports/` (not versioned).
- `LICENSE` added: PolyForm Noncommercial 1.0.0, with the notice `Required Notice: Copyright 2026 Fernando Neira-Roman`.
- Reading `config/config.yml` stays in each orchestrator. `templates/load_config.R` and `templates/load_config.py` are kept as the example of the function to extract when a second script needs the config.
- `templates/symlink_example.md` added (symbolic link commands; Linux/macOS tested, Windows not tested).
- README and `.gitignore` updated to match. The tree and steps below reflect this design.

### Changes from v1
- **Step 6 (critical 1):** the commented-out examples in `templates/main_template.R` (lines 41 and 44–46) are moved into an unexecuted `if (FALSE) { ... }` block so `commented_code_linter` passes.
- **Step 14 (critical 2):** literal rsync with trailing slashes and a dry run; **excluded by user instruction**.
- **Step 0:** aborts if `uv`, `air`, `rsync` or the R packages `yaml`, `purrr`, `readr`, `lintr` >= 3.2 are missing (`gh` is no longer needed).
- **Steps 8 and 9 swapped:** `.python-version` first, then `pyproject.toml` and `uv sync`.
- **Step 5:** `.gitignore` rules verified with `git check-ignore --no-index` in a scratch copy with `git init`.
- **Steps 4 and 11:** `reports/` (sources, versioned) vs `outputs/reports/` (renders, not versioned), documented in `config.yml` and the README. (Superseded by the 2026-10-27 amendment: sources now live in `src/reports/`.)
- **Step 13:** exact copies of the templates.

### Summary
Use the local tree as the base. Take from the remote what is useful (`.python-version`, `documents/status`, a reports folder). Remove what is unused or broken (JS, per-language loaders, package stub, METADATA.yaml, empty secrets). Fix internal contradictions on both sides. Publishing to GitHub is outside this plan.

### Assumptions
- No project-level CLAUDE.md; the global `~/.claude/CLAUDE.md` applies (English, one function per file, SCREAMING_SNAKE_CASE for constants, Black + Ruff 88, Google R 80, SSOT, purity, fail-fast).
- Python environment managed with `uv` (`.venv/lib/python3.12` present). Global R without `renv.lock`.
- TARGET_ROOT is not a git repo: a backup is made before any change.
- `out/`, `documents/*`, `src/functions/`, `data/*` contain only `.gitkeep`: restructuring them loses no data. (Checked during execution; see the execution log.)
- `templates/main_template.R` has commented-out code at lines 41 and 44–46; `.lintr` does not disable `commented_code_linter`.
- Commented-out code in `main_template.py` is not flagged: Ruff `ERA` is not selected.
- Correction to the original request: the remote `.gitignore` does **not** list `.secrets`; the file is versioned there and not ignored.
- Not verified at planning time: that lintr rejects `"SCREAMING_SNAKE_CASE"` as a style name. The local `.lintr` uses `"SNAKE_CASE"`, which in lintr means UPPER_SNAKE_CASE. Step 12 passing with that config is the evidence available.

### (a) Decisions

| # | Decision | Adopt | Why | Improvement over both |
|---|---|---|---|---|
| 1 | Output folder | `outputs/` with `figures/`, `tables/`, `reports/`. `models/` stays at the root. | The folder rule asks for full lowercase words; four local files already say `outputs/`. Models are inputs, not final outputs. | Adds `outputs/reports/` for rendered reports. |
| 2 | Configuration SSOT | A single `config/config.yml`, read directly by each orchestrator. No loaders. | YAML supports comments; the remote loaders duplicate the mapping per language and expose 2 of 9 keys. | Fail-fast check in both orchestrators if `config/config.yml` is missing. Secrets go in `.env`. |
| 3 | R dependencies | No renv in the template; opt-in per project (`renv::init()`). README lists `yaml`, `purrr`, `readr`. | A lockfile belongs to each project; spatial packages depend on system GDAL. | Correct `renv/` paths (the remote uses `.renv/`). |
| 4 | Role of Python | R and Python as equivalent scripting languages, not as a package. `[build-system]`, `[project.scripts]` and the stub are removed. | uv treats a project without a build system as a virtual project, which suits local analysis. | Symmetric commands: `Rscript src/main.R` and `uv run python src/main.py`. Imports `from functions.x import x`. |
| 5 | METADATA.yaml | Not adopted. | It describes no document and is in Spanish. | A project metadata block at the top of the README (plain text). Values a script needs go in `config/config.yml` (SSOT). Optional: `templates/document_template.md` with English front matter. |
| 6 | Stage folders | `documents/{plans,references,status}` | Plural like the rest; ebooks and papers are treated the same, so they merge into `references`. | `plans/` and `status/` versioned; only `references/` ignored. |
| 7 | Tests | None (out of scope). | YAGNI. | One line in the README on where they would go. |
| 8 | JS | Removed. | Out of scope. | — |
| 9 | Style tools | Black + Ruff (E, F, I, N, D google), 88 cols; `.lintr` (DCF) + `air.toml`; `commented_code_linter` active. pylint removed. | Black is required by the global CLAUDE.md (G0). The remote `.lintr` uses an invalid style name. | Black and Ruff pinned in a uv dev group and run with `uv run`. |
| 10 | Consumption | GitHub template. **Outside this plan** (manual publication by the user). | — | `.python-version` = 3.12, same as the local `.venv`. |

Final tree (current, after the 2026-10-27 amendment):

```
.env.example
.gitignore
.lintr
.python-version
air.toml
config/config.yml
data/{raw,interim,processed,external}/
documents/{plans,references,status}/
LICENSE
models/
outputs/{figures,tables,reports}/
pyproject.toml
README.md
src/functions/
src/reports/          # created when needed (report sources)
templates/            # function/main templates (R and Python), load_config.*, symlink_example.md
uv.lock
```

### (b) Steps

`ROOT` = `/Users/fneira/Documents/GITHUB/FOLDER_TEMPLATE`. `SCRATCH` = `/private/tmp/claude-501/-Users-fneira-Documents-GITHUB-FOLDER-TEMPLATE/34762d51-1202-4288-8361-3db864cc8f69/scratchpad`.

| # | Step | Command / file | Verification | Depends on | Risk | Data loss / breaks templates? |
|---|---|---|---|---|---|---|
| 0 | Preflight: back up ROOT and tools; **abort on any failure** | `rsync -a --exclude .venv/ --exclude .remember/ ROOT/ SCRATCH/folder-template-backup/`. Resolve `air`: `command -v air`, else the Positron bundle `/Users/fneira/.positron/extensions/posit.air-vscode-0.30.0/bundled/bin/air`, else abort. `for t in uv rsync; do command -v "$t" >/dev/null \|\| { echo "MISSING: $t"; exit 1; }; done`. `Rscript -e 'p <- c("yaml","purrr","readr","lintr"); m <- setdiff(p, rownames(installed.packages())); if (length(m)) stop("MISSING R pkgs: ", toString(m)); if (packageVersion("lintr") < "3.2.0") stop("lintr < 3.2.0")'` | `diff -rq` between ROOT and the backup (without `.venv`, `.remember`) is empty; the tool and package checks exit 0 | — | Low | No |
| 1 | Rename `out/` to `outputs/` and add `outputs/reports/` | `mv ROOT/out ROOT/outputs`; `mkdir -p ROOT/outputs/reports && touch ROOT/outputs/reports/.gitkeep` | `find ROOT/outputs -type f` lists 3 `.gitkeep`; `ROOT/out` does not exist | 0 | Low | No |
| 2 | Restructure `documents/` | `rm -r ROOT/documents/ebooks ROOT/documents/papers`; `mkdir ROOT/documents/references ROOT/documents/status`; `touch` a `.gitkeep` in each; keep `plans/` | `find ROOT/documents -type f` shows `.gitkeep` in plans, references, status | 0 | Low | No |
| 3 | Add `src/reports/`. *(Amended 2026-10-27: originally `reports/` at the root.)* | Not created at execution; created when the first report source is written | Folder exists when needed | 0 | Low | No |
| 4 | Update `config/config.yml` | Keep existing keys. Add `PATH_OUTPUTS_REPORTS: outputs/reports  # rendered reports, not versioned`. No `PATH_REPORTS` (removed 2026-10-27). Keep `ROI_NAME`, `CRS_OUTPUT`, `SEED` commented. | From ROOT: `Rscript -e 'cfg <- yaml::read_yaml("config/config.yml"); p <- unlist(cfg[grepl("^PATH_", names(cfg))]); stopifnot(all(dir.exists(p)))'` | 1 | Low | No |
| 5 | Fix `.gitignore` and verify it in a scratch repo | Replace the `documents/**` block with `documents/references/**`, `!documents/references/**/`, `!documents/references/**/.gitkeep`; add a "Reports" section with `.quarto/`; keep `outputs/**`, `data/**`, `models/**` and the secrets block. Check: `rsync -a --exclude .venv/ --exclude .remember/ ROOT/ SCRATCH/ignore-check/ && cd SCRATCH/ignore-check && git init -q && touch outputs/tables/x.csv documents/references/a.pdf documents/plans/p.md data/raw/r.tif models/m.rds .secrets` | `git check-ignore -v --no-index outputs/tables/x.csv documents/references/a.pdf data/raw/r.tif models/m.rds .secrets` reports a rule for all 5; `git check-ignore --no-index documents/plans/p.md outputs/tables/.gitkeep` prints nothing | 1, 2 | Medium | No |
| 6 | Update R templates (critical 1) | In `ROOT/templates/main_template.R`: (i) `scripts/functions` → `src/functions` in `@section`, comments and `list.files()`; (ii) before `read_yaml`, add `if (!file.exists("config/config.yml")) { stop("Run from the project root: config/config.yml not found.") }`; (iii) examples 1 and 2 stay as live code; examples 3 and 4 (lines 40–46) go into `# Alternative call patterns (not executed) ---` followed by `if (FALSE) {` ... `}`. `function_template.R` unchanged. | Step 12: `lintr::lint_dir()` clean; step 13 runs without executing the `if (FALSE)` block | 4 | Medium | Can break templates; steps 12 and 13 detect it |
| 7 | Update Python templates | In `ROOT/templates/main_template.py`: docstring `Run with uv run python src/main.py from the root`; import `from functions.function_name import function_name` (comment `src/functions/function_name.py`); before `yaml.safe_load`, add `if not Path("config/config.yml").is_file(): raise FileNotFoundError("Run from the project root: config/config.yml not found.")`. `function_template.py` unchanged. | Steps 12 and 13 | 4 | Medium | Can break templates; steps 12 and 13 detect it |
| 8 | Add `.python-version` | Create `ROOT/.python-version` with `3.12` | `cd ROOT && uv python find` resolves a 3.12.x | 0 | Low | No |
| 9 | Adjust and pin `pyproject.toml` | `name = "project-name"`; `requires-python = ">=3.12"`; `dependencies = ["pandas", "python-dotenv", "pyyaml"]`; add `[dependency-groups] dev = ["black", "ruff"]` and `[tool.ruff.lint.isort] known-first-party = ["functions"]`; keep Black/Ruff 88 and pydocstyle google sections. No `[build-system]`. Then `cd ROOT && uv lock && uv sync`. | `uv run python --version` gives 3.12.x; `uv run python -c "import pandas, yaml, dotenv"`; `uv run black --version` and `uv run ruff --version` work | 8 | Low | No (`.venv` and lock are regenerated) |
| 10 | (Optional, user decision) Document template | Create `ROOT/templates/document_template.md` with front matter `title`, `author: Fernando Neira-Roman`, `date`, `status: draft  # draft, final, superseded` | `uv run python -c "import yaml,pathlib; yaml.safe_load(pathlib.Path('templates/document_template.md').read_text().split('---')[1])"` | 9 | Low | No |
| 11 | Rewrite `README.md` (after 11a; names `.lintr` (DCF) as the lintr config) | Project metadata block at the top (title, author, status, date; plain text). A single "Conventions" section (naming table, Google R/Python references, 80/88 columns) as the human source. Tree from section (a) (current version). Start: `gh repo create <project-name> --template <your-github-user>/<template-repo> --private --clone`, **as a reference for the user only**, not run by the agent. Commands: `Rscript src/main.R`, `uv run python src/main.py`; style: `air format .`, `Rscript -e 'lintr::lint_dir()'`, `uv run ruff check . && uv run black --check .`. Dependencies: `uv add <pkg>`; R needs `yaml`, `purrr`, `readr`; opt-in renv with `renv::init()`. Reports: sources in `src/reports/` (versioned), renders in `outputs/reports/` (not versioned). One line on where tests would go. Versioning: data, models, outputs and `documents/references` not versioned; plans and status versioned. License section pointing to `LICENSE`. | `grep -nE 'scripts/|\bout/|output/' ROOT/README.md` empty; `grep -n 'reports/' ROOT/README.md` explains both locations | 1–10 | Low | No |
| 11a | Replace `.lintr.R` with `.lintr` (DCF); shorten convention comments in `pyproject.toml` and `air.toml` | Create `ROOT/.lintr` (DCF), with `linters: linters_with_defaults(` and indented continuation lines for `line_length_linter(80)`, `object_name_linter(styles = c("snake_case", "SNAKE_CASE"))`, `return_linter(return_style = "explicit")`, and `undesirable_function_linter(fun = c(attach = "use pkg::fun() or with()", setwd = "use project-relative paths from config/config.yml"))`, then `encoding: "UTF-8"`. Delete `ROOT/.lintr.R`. In `pyproject.toml` and `air.toml`, replace each convention block with `# Conventions: see README.md`, without changing executable config. | `test ! -e ROOT/.lintr.R`; step 12 validates `.lintr` | 9, 11 | Low | No |
| 12 | Static checks in ROOT | From ROOT (lintr reads the DCF `.lintr`): `air format --check .`; `Rscript -e 'l <- lintr::lint_dir(); print(l); stopifnot(length(l) == 0)'`; `uv run ruff check .`; `uv run black --check .` | All four exit 0. If lintr reports something, fix in steps 6/7; do not disable linters. A deliberate violation caught only by this config (e.g. `setwd("x")`, from `undesirable_function_linter`; `T` is not useful because it is already a default) in a disposable copy must be flagged, to confirm `.lintr` is read. | 6, 7, 9, 11 | Low | No |
| 13 | Smoke test of both orchestrators in a disposable copy | `rsync -a --exclude .venv/ --exclude .remember/ ROOT/ SCRATCH/smoke/ && cd SCRATCH/smoke`; copy the four templates into `src/` (`function_template.R` → `src/functions/function_name.R`, `main_template.R` → `src/main.R`, `function_template.py` → `src/functions/function_name.py`, `main_template.py` → `src/main.py`); `printf 'a,b\n1,2\n' > data/raw/t.csv`; `Rscript src/main.R`; `test -f outputs/tables/t.csv && rm outputs/tables/t.csv`; `uv run python src/main.py`; `test -f outputs/tables/t.csv` | Both runs exit 0 and write `outputs/tables/t.csv`. `cd src && Rscript main.R` fails with "Run from the project root" | 12 | Low | No (disposable copy only) |
| 14 | **EXCLUDED by user instruction:** GitHub publication | — | — | — | — | — |
| 15 | **EXCLUDED by user instruction:** mark the repo as a template | — | — | — | — | — |

### (c) Inconsistencies and how they were fixed

**Local**
1. README said `outputs/`; the folder was `out/`. Step 1.
2. `.gitignore` ignored `outputs/**`, so the contents of `out/` would have been versioned. Steps 1 and 5.
3. README, templates and `@section` said `scripts/`; the code lives in `src/functions/`. Steps 6, 7, 11.
4. README said `documents/` is versioned, but `.gitignore` ignored it entirely. Step 5.
5. Black was configured but not declared; README used `uvx` with no pinned version. Steps 9 and 11.
6. Unused dependencies (matplotlib, numpy, scipy, statsmodels). Step 9.
7. README had a `<user>/<template-repo>` placeholder. Step 11.
8. `name = "folder-template"` vs title `project-name`. Step 9.
9. `main_template.R` had commented-out code that `commented_code_linter` flags. Step 6.

**Remote (reference only; not modified)**
10. README tree listed files that do not exist. Replaced by the local README (publication is outside this plan).
11. `config.R` with a loose `list.files(...)`, undeclared `rprojroot`, `is_git_root` (fails outside git), undeclared `dotenv`. Loaders removed (decision 2).
12. Loaders did not match at the root and exposed 2 of 9 keys. Same fix.
13. `settings.json`: `DATA_PROCESSED` vs folder `data/preprocess`; `OUT_*` pointing to folders that do not exist; `PROJECT_NAME` in Spanish. Removed.
14. `.secrets` versioned and not ignored on the remote. Ignored by the local `.gitignore` (step 5).
15. `.env.copy` empty. Replaced by `.env.example`.
16. Remote `.gitignore` had wrong `.renv/` paths and no `data/external/` or `models/`. Local one adopted.
17. `.lintr` with the invalid style `"SCREAMING_SNAKE_CASE"`. Replaced by `.lintr` (DCF) using `"SNAKE_CASE"`.
18. Remote `pyproject.toml`: Python 3.14, 80 cols, placeholder `my_special_const`, pylint duplicating Ruff, uv_build stub. Steps 8 and 9.
19. Spanish content and empty placeholders. Removed.

**Between sources**
20. Three names for the output folder. Decision 1.
21. `plan`/`plans`/`ebooks`/`papers`/`references`. Decision 6.

### Known risks
- `if (FALSE)`: linted but not executed; if a future lintr version flags it, convert to prose, do not disable linters.
- Python imports work only with `uv run python src/main.py` from the root. Documented and tested in step 13.
- Missing tools: step 0 aborts before changing anything. `air` is resolved from PATH or from the Positron bundle (amended after execution).
- Versions: the lock pins Python versions; add `>=` floors if wanted.
- Black vs Ruff-only: a decision governed by the global CLAUDE.md.
- `templates/load_config.*` exists for a second consumer that does not exist yet. It is kept as a template example by user decision (2026-10-27).

---

## Pre-mortem

### Review v1
**Critical count**: 2
- Critical 1: `commented_code_linter` flags commented-out code in `main_template.R` (step 12 impossible). Resolved in v2 with the `if (FALSE)` block (step 6).
- Critical 2: step 14's rsync had no trailing slashes and no dry run. Resolved in v2, but the step is excluded by user instruction.

### Review v2 (verification)
**Critical count**: 1 (open at verification; fixed afterwards by editing the step 4 text to English, without re-verification)
- Critical: step 4 wrote Spanish comments into `config/config.yml`, against the English rule in the global CLAUDE.md. Fixed in the plan text.
- Resolved in v2: critical 1 from v1 (commented-out code in `main_template.R`, `if (FALSE)` block) and critical 2 from v1 (destructive rsync, excluded by user instruction).

### Amendment re-check (.lintr, metadata, conventions)
**Critical count**: 2 → 0 in the text (fixed after review; no re-verification)
- Critical 1: final tree, assumptions, inconsistency 17 and step 11 still referenced `.lintr.R`. Fixed.
- Critical 2: the `grep 'Google\|SNAKE'` check gave the opposite of the expected result. Rewritten as `grep -n 'Google'` plus a comment count.
- Minor items applied: literal `.lintr` format, a deliberate `setwd` violation test, METADATA check outside `documents/plans/`, step 11 after 11a.

### Re-verification after execution (2026-10-27)
Re-run on the current tree after the 2026-10-27 amendment:
- Step 12: `air format --check .`, `lintr::lint_dir()` (no lints), `ruff check .`, `black --check .`. All exit 0.
- Step 13: smoke test in a disposable copy. R and Python both write `outputs/tables/t.csv`. Running from `src/` fails with "Run from the project root: config/config.yml not found."

### Independent pre-mortem (2026-10-27, subagent review of the executed plan)
**Critical count**: 5 (as reported). Status of each:
1. The plan body was stale against the real tree → **fixed in this version** (tree, steps 3, 4, 11, verification).
2. The post-execution changes and the amendment had not been verified → **fixed**: steps 12 and 13 re-run and recorded above.
3. Step 0 assumed `air` on PATH → **fixed**: step 0 now resolves `air` from PATH or the Positron bundle. Recorded as MINOR (the execution itself passed).
4. No record of the execution approval → **fixed**: the user wrote "ejecuta el plan" on 2026-10-27 and confirmed the original authorization (A-01 answered "yes"). Recorded in the header.
5. Spanish content vs the global English rule → **fixed**: this plan and `documents/plans/LOG.md` are now in English, by user decision.

Open minor items: (a) `templates/__pycache__/` exists in the templates folder (generated when `load_config.py` was imported; ignore or delete, not part of the template). (b) Step 2 `rm -r` has no guard; it relied on the pre-verified `.gitkeep` assumption and on a backup in a session-temporary scratchpad. (c) Steps 1, 2 and 11a are not idempotent: do not re-run.

---

## Remaining limitations
- Steps 14 and 15 of the original v2 are not part of the execution: excluded by user instruction (manual publication).
- Windows symlink commands in `templates/symlink_example.md` are not tested on this machine (disclosed in the file).
- `templates/load_config.*` is not used by any orchestrator yet (kept as an example by user decision).
- Minor pre-mortem items listed above.

---

## Execution log
- Step 0: OK. Tools: `air` from the Positron path (0.12.0), `uv`, `rsync`, `git`, `Rscript`; R packages OK (lintr 3.3.0.1). Backup in `scratchpad/folder-template-backup/`. The original `command -v air` check did not resolve on this machine; the step was run with the Positron binary.
- Steps 1–3: `out/` → `outputs/` (only `.gitkeep`); `documents/` restructured (`ebooks/` and `papers/` removed, only `.gitkeep`; `references/` and `status/` created); `reports/` created at the time (later removed, see the 2026-10-27 amendment).
- Step 4: `config/config.yml` with `PATH_OUTPUTS_REPORTS` and `PATH_REPORTS` (English comments). The 9 `PATH_*` keys pointed to existing folders at the time. `PATH_REPORTS` later removed.
- Step 5: `.gitignore` with `documents/references/**` and a Reports section (`.quarto/`). Verified with `git check-ignore --no-index` in a scratch repo with `git init`.
- Step 6: `templates/main_template.R` with `src/functions`, fail-fast guard, and examples 3–4 inside `if (FALSE)`.
- Step 7: `templates/main_template.py` with `uv run python src/main.py`, `from functions.function_name import function_name`, fail-fast guard, comment updated to `functions.clean_data`.
- Step 8: `.python-version` = 3.12.
- Step 9: `pyproject.toml` with `name = "project-name"`, deps `pandas`, `python-dotenv`, `pyyaml`, dev group `black`/`ruff`, `known-first-party = ["functions"]`. `uv lock` and `uv sync` OK; Python 3.12.13.
- Step 10 (optional): skipped (user decision pending).
- Step 11a: `.lintr` (DCF) created and `.lintr.R` removed; `air.toml` and `pyproject.toml` reduced to a pointer to the README.
- Step 11: `README.md` rewritten with metadata, new structure, dependencies, reports, tests and conventions. Placeholder `<your-github-user>/<template-repo>` to fill in at publication.
- Step 12: `air format --check .`, `lintr::lint_dir()` (0 lints), `ruff check .`, `black --check .` pass.
- Step 13: smoke test in a copy: R and Python write `outputs/tables/t.csv`; fail-fast from `src/` gives the expected message; lintr detects `setwd` (proves `.lintr` is read).
- Extra: `tests/` removed (only `.gitkeep`; decision 7).
- Steps 14–15: excluded by user instruction (manual publication on GitHub).
- Result: **executed**.
- Amendment 2026-10-27 (user request): removed `reports/` at the root and `PATH_REPORTS`; report sources go in `src/reports/` (created when needed) and renders in `outputs/reports/`. README and `.gitignore` updated.
- Decision 2026-10-27: reading `config.yml` stays in the orchestrator (no `load_config()` extraction); both `main_template.*` have a "Config" section explaining how to read it and access keys. `templates/load_config.R` and `templates/load_config.py` kept as an example.
- Amendment 2026-10-27: `LICENSE` (PolyForm Noncommercial 1.0.0) and `templates/symlink_example.md` added; README updated with the tree, a link to the guide, and a license section.
- 2026-10-27 00:51: "ejecuta el plan" received. Approval recorded. Steps 0–13 not re-executed (they are done and not idempotent). Corrective actions applied to this document (tree, step 0, step 3, English translation) and verification re-run (steps 12 and 13, read-only / disposable copy) as described above.
