from pydantic import BaseModel, Field
from starlette.status import HTTP_404_NOT_FOUND


class ErrorSchema(BaseModel):
    """
    Base error scheme
    """

    result: bool = Field(default=False)
    error_type: int = Field(default=HTTP_404_NOT_FOUND)
    error_message: str = Field(default="Not found")


class ErrorOut(BaseModel):
    """
    A model that contains error details
    """

    details: ErrorSchema
