async def test_healthcheck(client):
    response = await client.get("/healthcheck")
    assert response.status_code == 200
