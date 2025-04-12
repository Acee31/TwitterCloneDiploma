import os
import uuid
from typing import Tuple

from fastapi import HTTPException, UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.db.models import Image


IMAGE_UPLOAD_DIR = "/home/static/images"


async def upload_image(session: AsyncSession, file: UploadFile) -> Tuple[bool, int]:
    """
    Uploads an image file to the server, saves it in the specified directory,
    and stores the image's path in the database.

    :param session: The database session used for the query
    :param file: The file objects of type 'UploadFile' containing the image to be uploaded
    :return: Tuple (bool, int). The tuple returns a bool and the image ID on a successful request
    """
    try:
        filename = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(IMAGE_UPLOAD_DIR, filename)

        os.makedirs(IMAGE_UPLOAD_DIR, exist_ok=True)

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        public_path = f"images/{filename}"
        image = Image(path=public_path)
        session.add(image)
        await session.commit()
        return True, image.id
    except SQLAlchemyError:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "result": False,
                "error_type": HTTP_500_INTERNAL_SERVER_ERROR,
                "error_message": "Database error",
            },
        )
