from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ErrorResponse(BaseModel):
    detail: str
    error_code: str = "bad_request"


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class PageMeta(BaseModel):
    page: int
    page_size: int
    total: int


class PaginatedResponse(BaseModel):
    items: list[dict]
    meta: PageMeta
