import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent


def get_env_file_path():
    match os.environ.get("ENV", "local"):
        case "local":
            env_file = ROOT_DIR.parent.parent / ".env"
        case _:
            env_file = Path("/opt/.env")
    return env_file
