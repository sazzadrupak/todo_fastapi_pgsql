'''
Schema for book
'''

from typing import Optional
from pydantic import BaseModel, Field


class BookRequest(BaseModel):
    '''Data model for book request'''
    id: Optional[int] = Field(
        description='Id is not neede on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "sazzad",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2029
            }
        }
    }
