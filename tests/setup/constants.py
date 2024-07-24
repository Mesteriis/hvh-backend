from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.parent.resolve()
SRC_RATH = ROOT_PATH / "src"
TESTS_PATH = ROOT_PATH / "tests"

TEST_MEDIA_FOLDER = TESTS_PATH / "media"
TEST_MEDIA_FOLDER.mkdir(parents=True, exist_ok=True)


DB_URI_IN_MEMORY: str = "sqlite://:memory:"
DB_URI_FILE: str = f"sqlite://{TESTS_PATH}test.db"
DB_URI_POSTGRES: str = "postgres://tortoise:tortoise@localhost:8432/tortoise_test"  # noqa:  PostgreSQL database
