"""
Service for user
"""
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.models.user import User
from app.utils.hash import Hash


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    result = await db.execute(
        text('SELECT * FROM USERS WHERE id = :user_id'),
        {'user_id': user_id}
    )
    return result.mappings().fetchone()


async def change_password(db: AsyncSession, user_id: int, password: str):
    await db.execute(
        text('''
             UPDATE users
             SET
                hashed_password = :password,
                token_version = token_version + 1
             WHERE id = :user_id
        '''),
        {'password': password, 'user_id': user_id}
    )
    await db.commit()


async def update_phone_number(db: AsyncSession, user_id: int, phone_number: str):
    await db.execute(
        text('''
             UPDATE users
             SET phone_number = :phone_number
             WHERE id = :user_id
        '''),
        {'phone_number': phone_number, 'user_id': user_id}
    )
    await db.commit()


# async def update_user(user_id: int, user: UserUpdate, db: AsyncSession):
#     print('user_data', user)
#     user_repo = UserRepository(db)
#     existing_user = await user_repo.get_user_by_id(user_id)
#     if existing_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     for key, value in user.dict().items():
#         setattr(existing_user, key, value)
#     updated_user = await user_repo.update_user(user_id, existing_user)
#     return UserResponse.from_orm(updated_user)

# async def get_user_by_email(db, email: str) -> User:
#     result = await db.execute(select(User).where(User.email == email))
#     return result.scalars().first()


# async def create_user(request: UserBase, db: AsyncSession):
#     existing_user = await get_user_by_email(db, request.email)
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     user = User(
#         name=request.name,
#         email=request.email,
#         hashed_password=Hash.bcrypt(request.password)
#     )

#     db.add(user)
#     await db.commit()
#     await db.refresh(user)
#     return user


# async def get_all_users(db: AsyncSession) -> List[User]:
#     result = await db.execute(select(User))
#     return result.scalars().all()
