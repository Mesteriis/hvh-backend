import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

MEDIA_FOLDER = ROOT_DIR / "media"
MEDIA_FOLDER.mkdir(exist_ok=True)

LOGS_FOLDER = ROOT_DIR / "logs"
LOGS_FOLDER.mkdir(exist_ok=True)
