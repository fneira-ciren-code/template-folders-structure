git remote add origin https://github.com/fneira-ciren-code/template-folders-structure.git
git branch -M main
git push -u origin main


my-hybrid-project/
├── .git/
├── .gitignore               # Multi-language ignore (Python, R, JS/Node, OS)
├── .editorconfig            # Enforces unified indentation and line-endings
├── .lintr                   # R linting config (Google Style aligned)
├── .prettierrc              # Unified formatting for JS, TS, JSON, YAML, Markdown
├── .python-version          # Python version lock
├── pyproject.toml           # Python dependencies + Ruff config (Google Python Style)
├── package.json             # JS/TS dependencies + ESLint/Prettier setup
├── renv.lock                # R reproducible environment lockfile
├── Justfile                 # Task runner for R, Python, and JS execution
├── README.md
├── main.py                  # Entry point: Python pipeline
├── main.R                   # Entry point: R pipeline
├── main.js                  # Entry point: JavaScript/Node pipeline
├── config/                  # Central config directory (paths, envs, secrets loader)
│   ├── settings.json        # Base static configuration & shared path map
│   ├── .env.example         # Secret/environment template
│   ├── config.py            # Python config loader
│   ├── config.R             # R config loader
│   └── config.js            # JavaScript config loader
├── data/                    # Shared data tiers
│   ├── raw/
│   ├── interim/
│   └── processed/
├── src/                     # Core reusable modules grouped by language/purpose
│   ├── py/                  # Internal Python packages/modules
│   ├── r/                   # Internal R functions/scripts
│   └── js/                  # Internal JS/TS modules
├── notebooks/               # Multi-language notebooks (Jupyter / Quarto / Rmd)
└── tests/                   # Multi-language test suite
    ├── py/
    ├── r/
    └── js/