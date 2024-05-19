from typing import Optional

from pydantic import BaseModel, Field


class BookSchema(BaseModel):
    title: str = Field(...)
    author: str = Field(...)
    category: str = Field(...)
    year: int = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "category": "Novel",
                "year": 1925,
            }
        }


class UpdateBookModel(BaseModel):
    title: Optional[str]
    author: Optional[str]
    category: Optional[str]
    year: Optional[int]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "category": "Novel",
                "year": 1925,
            }
        }


def ResponseModel(data, message):
    return {"data": [data], "code": 200, "message": message}


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
