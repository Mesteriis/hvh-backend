from pathlib import Path

import pytest

from tools.email_inspectors.inspector import EmailInspector


@pytest.fixture
def client() -> EmailInspector:
    return EmailInspector()


@pytest.fixture
def file_path() -> Path:
    return Path(__file__).parent / 'emails.xlsx'

