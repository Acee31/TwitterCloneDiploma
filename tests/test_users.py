from httpx import AsyncClient

API_HEADER = {"api-key": "test"}


async def test_get_me(client: AsyncClient):
    response = await client.get("/api/users/me", headers=API_HEADER)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"] is True
    assert data["user"]["name"] == "User3"
    assert isinstance(data["user"]["followers"], list)


async def test_get_by_id(client: AsyncClient):
    response = await client.get("/api/users/1")
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"] is True
    assert isinstance(data["user"]["followers"], list)
    assert data["user"]["name"] != "User2"
    assert data["user"]["name"] != "User3"
    assert data["user"]["name"] == "User1"


async def test_follow_user(client: AsyncClient):
    response = await client.post("/api/users/2/follow", headers=API_HEADER)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"] is True

    response = await client.post("/api/users/1/follow", headers=API_HEADER)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"]["error_message"] == "Already following this user"

    response = await client.post("/api/users/99999/follow", headers=API_HEADER)
    assert response.status_code == 404
    data = response.json()
    assert "to follow not found" in data["detail"]["error_message"]


async def test_unfollow_user(client: AsyncClient):
    response = await client.delete("/api/users/1/follow", headers=API_HEADER)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"] is True

    response = await client.delete("/api/users/2/follow", headers=API_HEADER)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"]["error_message"] == "Not following this user"

    response = await client.delete("/api/users/3/follow", headers=API_HEADER)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"]["error_message"] == "Cannot unfollow yourself"
