import pytest


pytestmark = pytest.mark.api


async def test_get_tasks(client, task_factory):
    user = await client.force_auth()
    task = await task_factory.create(owner_id=user.id)
    url = client.url_for("get_list_tasks")
    response = await client.get(url)
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": str(task.id),
            "url": task.url,
            "owner_id": str(task.owner_id)
        }
    ], f"Error {response.json()}"


async def test_create_task(client):
    await client.force_auth()
    url = client.url_for("create_task")
    response = await client.post(url, json={"url": "https://test.com"})
    assert response.status_code == 200, f"Error {response.json()}"


async def test_get_task(client, task_factory):
    user = await client.force_auth()
    task = await task_factory.create(owner_id=user.id)
    url = client.url_for("get_task", task_id=task.id)
    response = await client.get(url)
    assert response.status_code == 200, f"Error {response.json()}"
