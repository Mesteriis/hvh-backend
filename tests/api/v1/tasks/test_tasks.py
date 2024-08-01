import uuid

import pytest

from tests.setup.inventory.factories import UserModelFactory, TaskModelFactory

pytestmark = pytest.mark.api


async def test_get_tasks(client):
    user = await UserModelFactory.create()
    task = await TaskModelFactory.create(owner_id=user.id)
    url = client.url_for("get_list_tasks")
    response = await client.get(url)
    assert response.status_code == 200
    assert response.json() == [
        {"id": task.id, "url": task.url, "owner_id": str(task.owner_id)}
    ], f"Error {response.json()}"


async def test_create_task(client):
    user = await UserModelFactory.create()
    data = {"url": "https://test.com"}
    url = client.url_for("create_task")
    await client.force_auth(user)
    response = await client.post(url, json=data)
    assert response.status_code == 200, f"Error {response.json()}"

def test_get_task(client):
    assert False
