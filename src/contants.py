from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

MEDIA_FOLDER = ROOT_DIR / "media"
MEDIA_FOLDER.mkdir(exist_ok=True)

LOGS_FOLDER = ROOT_DIR / "logs"
LOGS_FOLDER.mkdir(exist_ok=True)

APP_FOLDER = ROOT_DIR / "src"

STATIC_FOLDER = APP_FOLDER / "static"
STATIC_FOLDER.mkdir(exist_ok=True)

TEMPLATES_FOLDER = APP_FOLDER / "templates"
TEMPLATES_FOLDER.mkdir(exist_ok=True)
