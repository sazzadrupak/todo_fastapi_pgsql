from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.schemas.auth import CreateUserRequest
from app.models.user import User
from app.utils.hash import Hash


async def create_user(request: CreateUserRequest, db: AsyncSession):
    print('USER ROLE', request.role)
    user_model = User(
        email=request.email,
        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        role=request.role,
        hashed_password=Hash.bcrypt(request.password),
        is_active=True,
        token_version=1,
        phone_number=request.phone_number
    )
    db.add(user_model)
    await db.commit()


async def get_user_by_username(username: str, db: AsyncSession):
    result = await db.execute(
        text('SELECT * FROM users WHERE username = :username'),
        {'username': username}
    )
    return result.mappings().fetchone()
