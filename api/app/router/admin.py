from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services import admin
from app.router.auth import get_current_user


router = APIRouter()

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

db_dependency = Annotated[AsyncSession, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/todos', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    '''Get all todos'''
    print('USER', user)
    if user is None or user.get('role') != 'admin':
        raise HTTPException(
            status_code=401,
            detail='Authentication Failed'
        )
    return await admin.get_all_todos(db)


@router.delete('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency,
    db: db_dependency,   # type: ignore
    todo_id: int = Path(gt=0)
):
    '''Delete a todo'''
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication failed!')

    todo = await admin.get_todo_by_id(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail='Todo item not found')
    await admin.delete_todo(db, todo_id)
