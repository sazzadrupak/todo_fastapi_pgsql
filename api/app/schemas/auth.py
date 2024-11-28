from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class UserRole(Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'


class CreateUserRequest(BaseModel):
    email: str
    username: str
    password: str = Field(min_length=3)
    first_name: str
    last_name: str
    role: UserRole
    phone_number: str

    model_config = ConfigDict(
        use_enum_values=True,
        extra="forbid",
        json_schema_extra={
            "example": {
                "email": "example@example.com",
                "username": "example",
                "first_name": "First",
                "last_name": "Last",
                "password": "1234ABCD",
                "role": "USER",
                "phone_number": '+358417169112'
            }
        }
    )


class Token(BaseModel):
    access_token: str
    token_type: str
