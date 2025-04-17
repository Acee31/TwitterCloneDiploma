import os
from httpx import AsyncClient


API_HEADER = {"api-key": "test"}


async def test_upload_image(client: AsyncClient):
    test_image_path = os.path.join(os.path.dirname(__file__), "../static/images/cosmos_1.jpg")
    assert os.path.exists(test_image_path), f"Test image file does not exist at {test_image_path}"

    with open(test_image_path, "rb") as image:
        response = await client.post(
            "/api/medias",
            headers=API_HEADER,
            files={"file": ("cosmos_1.jpg", image, "image/jpeg")}
        )

    assert response.status_code == 200
