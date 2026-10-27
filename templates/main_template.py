"""main.py: thin orchestrator. Run with `uv run python src/main.py` from the root."""

from pathlib import Path

import pandas as pd
import yaml
from dotenv import load_dotenv

# Import functions: one import per file in src/functions/.
# Each file defines one function with the same name, so
# `src/functions/function_name.py` -> `function_name()`.
from functions.function_name import function_name

# from functions.clean_data import clean_data

# Config -----------------------------------------------------------------------
# Single read of config/config.yml (SSOT, read-only). When another script needs
# it (for example a report in src/reports/), copy templates/load_config.py to
# src/functions/ and call load_config(). Keys are read as CONFIG["PATH_DATA_RAW"],
# CONFIG["PATH_OUTPUTS_TABLES"], and so on.
CONFIG_PATH = Path("config/config.yml")
if not CONFIG_PATH.is_file():
    raise FileNotFoundError("Run from the project root: config/config.yml not found.")

CONFIG = yaml.safe_load(CONFIG_PATH.read_text())
load_dotenv()


def main() -> None:
    """Run the pipeline."""
    # Input (I/O at the edge)
    input_files = sorted(Path(CONFIG["PATH_DATA_RAW"]).glob("*.csv"))
    if not input_files:
        raise FileNotFoundError(f"No CSV files in {CONFIG['PATH_DATA_RAW']}.")

    raw_list = [pd.read_csv(path) for path in input_files]

    # 1. Single call
    # result = function_name(raw_list[0])

    # 2. Vectorised call over many inputs (one result per input file)
    result_list = [function_name(df) for df in raw_list]

    # 3. Call with extra arguments
    # result_list = [function_name(df, k=3) for df in raw_list]

    # 4. Chaining several functions
    # result_list = [function_name(clean_data(df)) for df in raw_list]

    # Output (I/O at the edge)
    output_dir = Path(CONFIG["PATH_OUTPUTS_TABLES"])
    for df, path in zip(result_list, input_files):
        df.to_csv(output_dir / path.name, index=False)


if __name__ == "__main__":
    main()
