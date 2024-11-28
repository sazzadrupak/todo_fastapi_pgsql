from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
# import httpx
from typing import List, Annotated
from typing import Annotated

from app.schemas.user import UserPasswordVerification
from app.db.session import get_db
from app.router.auth import get_current_user
from app.services import users
from app.utils.hash import Hash


router = APIRouter(
    prefix='/user',
    tags=['user'],
)

db_dependency = Annotated[AsyncSession, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    '''Get user'''
    return await users.get_user_by_id(db, user_id=user.get('id'))


@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency,
    db: db_dependency,
    user_verification: UserPasswordVerification
):
    """Update user's password"""
    user_model = await users.get_user_by_id(db, user_id=user.get('id'))

    if not Hash.verify(user_model.hashed_password, user_verification.password):
        raise HTTPException(status_code=401, detail='Error on password change')
    await users.change_password(db, user_id=user_model.id, password=Hash.bcrypt(user_verification.new_password))


@router.put('/phone_number', status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, phone_number: str):
    """Update user's phone number"""
    await users.update_phone_number(db, user_id=user.get('id'), phone_number=phone_number)


# @router.post('/', response_model=UserResponse)
# async def create_new_user(request: UserBase, db: AsyncSession = Depends(get_db)):
#     return await user_service.create_user(request, db)
# async def update_user(user_id: int, request: UserUpdate, db: AsyncSession = Depends(get_db)):
#     return await user_service.update_user(user_id, request, db)
# async with httpx.AsyncClient() as client:
#   response = await client.get('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
#   users = response.json()
# api_url = "https://jsonplaceholder.typicode.com/users"
# async with httpx.AsyncClient() as client:
#   response = await client.get(api_url)
#   users = response.json()
#   return users
