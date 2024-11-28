'''
Schema for todos
'''

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class TodosRequest(BaseModel):
    '''Data model for todos request'''
    title: str = Field(min_length=3)
    description: str = Field(min_length=1, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "title": "A new book",
                "description": "A new description of a book",
                "priority": 5,
                "complete": False
            }
        }
    )
