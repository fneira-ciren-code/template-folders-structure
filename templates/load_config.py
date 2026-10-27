"""load_config.py: reads the project configuration file."""

from pathlib import Path

import yaml


def load_config(path: str = "config/config.yml") -> dict:
    """Load the project configuration.

    Args:
        path: Path to the YAML config file, relative to the project root.

    Returns:
        Dict with the config keys (SCREAMING_SNAKE_CASE).

    Raises:
        FileNotFoundError: If the file does not exist (usually the script was
            not run from the project root).
    """
    config_path = Path(path)
    if not config_path.is_file():
        raise FileNotFoundError(f"Run from the project root: {path} not found.")

    return yaml.safe_load(config_path.read_text())
