"""
Tests for API tweets.

This module contains tests for:
- Get all tweets
- Add a like
- Delete a like
- Create a tweet
- Delete a tweet
"""

from http import HTTPStatus
from types import MappingProxyType

from httpx import AsyncClient

API_HEADER = MappingProxyType({"api-key": "test"})


async def test_get_all_tweets(client: AsyncClient):
    """
    Test retrieving all tweets.

    Ensures the endpoint returns a list of tweets with expected structure and length.
    :param client: Async test client for API interaction
    """
    response = await client.get("/api/tweets", headers=API_HEADER)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "result" in data
    assert data["result"] is True
    assert isinstance(data["tweets"], list)
    assert len(data["tweets"]) == 3


async def test_like_tweet(client: AsyncClient):
    """
    Test liking a tweet.

    - Successful like
    - Duplicate like
    - Like on non-existent tweet

    :param client: Async test client for API interaction
    """
    response = await client.post("/api/tweets/1/likes", headers=API_HEADER)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "result" in data
    assert data["result"] is True

    response = await client.post("/api/tweets/1/likes", headers=API_HEADER)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.json()
    assert data["detail"]["error_message"] == "Already liked this tweet"

    response = await client.post("/api/tweets/9999/likes", headers=API_HEADER)
    assert response.status_code == HTTPStatus.NOT_FOUND
    data = response.json()
    assert data["detail"]["error_message"] == "Tweet with id 9999 not found"


async def test_delete_like(client: AsyncClient):
    """
    Test removing a like from a tweet.

    - Successful removal
    - Attempt to remove like twice
    - Attempt to remove like from non-existent tweet

    :param client: Async test client for API interaction
    """
    response = await client.delete("/api/tweets/3/likes", headers=API_HEADER)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "result" in data
    assert data["result"] is True

    response = await client.delete("/api/tweets/3/likes", headers=API_HEADER)
    assert response.status_code == HTTPStatus.NOT_FOUND
    data = response.json()
    assert "result" in data["detail"]
    assert data["detail"]["result"] is False
    assert data["detail"]["error_message"] == "Tweet with id 3 doesn't have a like"

    response = await client.delete("/api/tweets/9999/likes", headers=API_HEADER)
    assert response.status_code == HTTPStatus.NOT_FOUND
    data = response.json()
    assert "result" in data["detail"]
    assert data["detail"]["result"] is False
    assert data["detail"]["error_message"] == "Tweet with id 9999 not found"


async def test_create_tweet(client: AsyncClient):
    """
    Test creating a new tweet.

    Sends valid tweet data and checks that the tweet is successfully created.
    :param client: Async test client for API interaction
    """
    text = {"tweet_data": "test"}
    response = await client.post("/api/tweets", headers=API_HEADER, json=text)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "result" in data
    assert data["result"] is True
    assert "tweet_id" in data
    assert isinstance(data["tweet_id"], int)
    assert data["tweet_id"] == 4


async def test_delete_tweet(client: AsyncClient):
    """
    Test deleting a tweet.

    - Successful deletion
    - Attempt to delete someone else's tweet
    - Attempt to delete non-existent tweet

    :param client: Async test client for API interaction
    """
    response = await client.delete("/api/tweets/3", headers=API_HEADER)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "result" in data
    assert data["result"] is True

    response = await client.delete("/api/tweets/1", headers=API_HEADER)
    assert response.status_code == HTTPStatus.FORBIDDEN
    data = response.json()
    assert "result" in data["detail"]
    assert data["detail"]["result"] is False
    assert data["detail"]["error_message"] == "You cannot delete this tweet"

    response = await client.delete("/api/tweets/9999", headers=API_HEADER)
    assert response.status_code == HTTPStatus.NOT_FOUND
    data = response.json()
    assert "result" in data["detail"]
    assert data["detail"]["result"] is False
    assert data["detail"]["error_message"] == "Not found tweet with id 9999"
