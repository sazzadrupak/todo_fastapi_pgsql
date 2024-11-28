"""
Todos APIs
"""
from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services import todos
from app.schemas.todos import TodosRequest
from app.router.auth import get_current_user


router = APIRouter(
    prefix='/todos',
    tags=['todos']
)

db_dependency = Annotated[AsyncSession, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_todos(user: user_dependency, db: db_dependency):  # type: ignore
    '''Return Todos list'''
    return await todos.get_all_todos(db, owner_id=user.get('id'))


@router.get('/{todo_id}', status_code=status.HTTP_200_OK)
async def get_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):  # type: ignore
    '''Get toto by id'''
    todo = await todos.get_todo_by_id(db, todo_id, owner_id=user.get('id'))
    if todo is None:
        raise HTTPException(status_code=404, detail='Todo item not found')
    return todo


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency,
    db: db_dependency,   # type: ignore
    todo_req: TodosRequest
):
    '''Create a new todo'''
    await todos.create_todo(db, todo_request=todo_req, owner_id=user.get('id'))


@router.put('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,   # type: ignore
    todo_request: TodosRequest,
    todo_id: int = Path(gt=0)
):
    '''Update a todo'''
    todo = await todos.get_todo_by_id(db, todo_id, owner_id=user.get('id'))
    if todo is None:
        raise HTTPException(status_code=404, detail='Todo item not found')
    await todos.update_todo(db, todo_id, todo_request, owner_id=user.get('id'))


@router.delete('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency,
    db: db_dependency,   # type: ignore
    todo_id: int = Path(gt=0)
):
    '''Delete a todo'''
    todo = await todos.get_todo_by_id(db, todo_id, owner_id=user.get('id'))
    if todo is None:
        raise HTTPException(status_code=404, detail='Todo item not found')
    await todos.delete_todo(db, todo_id, owner_id=user.get('id'))
