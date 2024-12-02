from pathlib import Path

import pytest

from tools.email_inspectors.inspector import EmailInspector


@pytest.fixture
def client() -> EmailInspector:
    return EmailInspector()


@pytest.fixture
def file_path() -> Path:
    return Path(__file__).parent / 'emails.xlsx'


def test_inspector(client, file_path):
    client.read_xlsx(file_path)
    print(client.stat())
    client.execute()
    print(client.stat())
