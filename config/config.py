import json
import os
from pathlib import Path

# pyrefly: ignore[missing-import]
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / "config" / "settings.json") as f:
    _SETTINGS = json.load(f)

# Global Constants (SCREAMING_SNAKE_CASE)
DIR_DATA_RAW = BASE_DIR / _SETTINGS["PATHS"]["DATA_RAW"]
DIR_DATA_PROCESSED = BASE_DIR / _SETTINGS["PATHS"]["DATA_PROCESSED"]
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "")
