from httpx import AsyncClient

API_HEADER = {"api-key": "test"}


async def test_get_all_tweets(client: AsyncClient):
    response = await client.get("/api/tweets", headers=API_HEADER)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"] is True
    assert isinstance(data["tweets"], list)
    assert len(data["tweets"]) == 3


async def test_like_tweet(client: AsyncClient):
    response = await client.post("/api/tweets/1/likes", headers=API_HEADER)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"] is True

    response = await client.post("/api/tweets/1/likes", headers=API_HEADER)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"]["error_message"] == "Already liked this tweet"

    response = await client.post("/api/tweets/9999/likes", headers=API_HEADER)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"]["error_message"] == "Tweet with id 9999 not found"


async def test_delete_like(client: AsyncClient):
    response = await client.delete("/api/tweets/3/likes", headers=API_HEADER)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"] is True

    response = await client.delete("/api/tweets/3/likes", headers=API_HEADER)
    assert response.status_code == 404
    data = response.json()
    assert "result" in data["detail"]
    assert data["detail"]["result"] is False
    assert data["detail"]["error_message"] == "Tweet with id 3 doesn't have a like"

    response = await client.delete("/api/tweets/9999/likes", headers=API_HEADER)
    assert response.status_code == 404
    data = response.json()
    assert "result" in data["detail"]
    assert data["detail"]["result"] is False
    assert data["detail"]["error_message"] == "Tweet with id 9999 not found"


async def test_create_tweet(client: AsyncClient):
    text = {"tweet_data": "test"}
    response = await client.post("/api/tweets", headers=API_HEADER, json=text)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"] is True
    assert "tweet_id" in data
    assert isinstance(data["tweet_id"], int)
    assert data["tweet_id"] == 4


async def test_delete_tweet(client: AsyncClient):
    response = await client.delete("/api/tweets/3", headers=API_HEADER)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"] is True

    response = await client.delete("/api/tweets/1", headers=API_HEADER)
    assert response.status_code == 403
    data = response.json()
    assert "result" in data["detail"]
    assert data["detail"]["result"] is False
    assert data["detail"]["error_message"] == "You cannot delete this tweet"

    response = await client.delete("/api/tweets/9999", headers=API_HEADER)
    assert response.status_code == 404
    data = response.json()
    assert "result" in data["detail"]
    assert data["detail"]["result"] is False
    assert data["detail"]["error_message"] == "Not found"
