"""This module contains API-function for image."""

from typing import Annotated, Any, Dict

from fastapi import APIRouter, Depends, Header, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_settings import db_session
from app.db.schemas.error_schemas import ErrorOut
from app.db.schemas.tweet_schemas import ImageSchema
from app.routes.crud.crud_images import upload_image

medias_routes = APIRouter(prefix="/api/medias", tags=["Operation with medias"])


@medias_routes.post(
    "",
    response_model=ImageSchema,
    responses={
        500: {"model": ErrorOut},
    },
    summary="Upload medias",
    description="Endpoint for uploading images",
)
async def upload_media(
    file: UploadFile,
    api_key: Annotated[str, Header(description="User API key")],
    session: Annotated[AsyncSession, Depends(db_session.get_session)],
) -> Dict[str, Any]:
    """Upload a media file to the server and return its ID."""
    result, image_id = await upload_image(session=session, file=file)
    return {"result": result, "media_id": image_id}
