from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    skip: int
    limit: int
    has_more: bool = False


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
