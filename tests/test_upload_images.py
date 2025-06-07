"""
Tests for API users.

This module contains tests for:
- Upload image
"""

import os
from http import HTTPStatus
from types import MappingProxyType

from httpx import AsyncClient

API_HEADER = MappingProxyType({"api-key": "test"})


async def test_upload_image(client: AsyncClient):
    """
    Test uploading an image.

    Checks that the endpoint successfully accepts and processes the file
    :param client: Async test client for API interaction
    """
    test_image_path = os.path.join(
        os.path.dirname(__file__),
        "../static/images/cosmos_1.jpg",
    )

    with open(test_image_path, "rb") as image:
        response = await client.post(
            "/api/medias",
            headers=API_HEADER,
            files={"file": ("cosmos_1.jpg", image, "image/jpeg")},
        )

    assert response.status_code == HTTPStatus.OK
