"""
Tests for API users.

This module contains tests for:
- Getting current user
- Getting by ID
- Subscription and unsubscription
"""

from http import HTTPStatus
from types import MappingProxyType

from httpx import AsyncClient

API_HEADER = MappingProxyType({"api-key": "test"})


async def test_get_me(client: AsyncClient):
    """
    Test retrieving the authenticated user's information.

    Includes checks for valid and invalid API key usage.
    :param client: Async test client for API interaction
    """
    response = await client.get("/api/users/me", headers=API_HEADER)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "result" in data
    assert data["result"] is True
    assert data["user"]["name"] == "User3"
    assert isinstance(data["user"]["followers"], list)
    assert isinstance(data["user"]["following"], list)

    response = await client.get("/api/users/me", headers={"api-key": "fail"})
    assert response.status_code == HTTPStatus.NOT_FOUND
    data = response.json()
    assert data["detail"]["error_message"] == "Not found user with api-key/id: fail"


async def test_get_by_id(client: AsyncClient):
    """
    Test retrieving user information by user ID.

    Includes checks for valid and invalid IDs.
    :param client: Async test client for API interaction
    """
    response = await client.get("/api/users/1")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "result" in data
    assert data["result"] is True
    assert isinstance(data["user"]["followers"], list)
    assert data["user"]["name"] != "User2"
    assert data["user"]["name"] != "User3"
    assert data["user"]["name"] == "User1"

    response = await client.get("/api/users/9999")
    assert response.status_code == HTTPStatus.NOT_FOUND
    data = response.json()
    assert data["detail"]["error_message"] == "Not found user with api-key/id: 9999"


async def test_follow_user(client: AsyncClient):
    """
    Test following another user by user ID.

    Includes checks for:
    - Successful follow
    - Following a non-existent user
    - Following an already followed user
    - Attempting to follow oneself
    :param client: Async test client for API interaction
    """
    response = await client.post("/api/users/1/follow", headers=API_HEADER)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "result" in data
    assert data["result"] is True

    response = await client.post("/api/users/9999/follow", headers=API_HEADER)
    assert response.status_code == HTTPStatus.NOT_FOUND
    data = response.json()
    assert data["detail"]["error_message"] == "User with id 9999 to follow not found"

    response = await client.post("/api/users/1/follow", headers=API_HEADER)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.json()
    assert data["detail"]["error_message"] == "Already following this user"

    response = await client.post("/api/users/99999/follow", headers=API_HEADER)
    assert response.status_code == HTTPStatus.NOT_FOUND
    data = response.json()
    assert "to follow not found" in data["detail"]["error_message"]

    response = await client.post("/api/users/3/follow", headers=API_HEADER)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.json()
    assert data["detail"]["error_message"] == "Cannot follow yourself"


async def test_unfollow_user(client: AsyncClient):
    """
    Test unfollowing a user by user ID.

    Includes checks for:
    - Successful unfollow
    - Unfollowing a non-existent user
    - Unfollowing a user not currently followed
    - Attempting to unfollow oneself
    :param client: Async test client for API interaction
    """
    response = await client.delete("/api/users/2/follow", headers=API_HEADER)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "result" in data
    assert data["result"] is True

    response = await client.delete("/api/users/9999/follow", headers=API_HEADER)
    assert response.status_code == HTTPStatus.NOT_FOUND
    data = response.json()
    assert data["detail"]["error_message"] == "Not found user with api-key/id: 9999"

    response = await client.delete("/api/users/2/follow", headers=API_HEADER)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.json()
    assert data["detail"]["error_message"] == "Not following this user"

    response = await client.delete("/api/users/3/follow", headers=API_HEADER)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.json()
    assert data["detail"]["error_message"] == "Cannot unfollow yourself"
