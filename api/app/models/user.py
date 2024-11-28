from sqlalchemy import Column, Integer, String, Boolean, Enum as SqlEnum

from app.db.session import Base
from app.schemas.auth import UserRole


def get_enum_values(enum_class):
    return [member.value for member in enum_class]


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(
        SqlEnum(UserRole, values_callable=get_enum_values, native_enum=False))
    token_version = Column(Integer)
    phone_number = Column(String)
