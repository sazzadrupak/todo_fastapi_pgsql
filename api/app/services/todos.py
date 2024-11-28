from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi import HTTPException

from app.schemas.todos import TodosRequest
from app.models.todos import Todos


async def get_all_todos(db: AsyncSession, owner_id: int):
    result = await db.execute(
        text('SELECT * FROM todos WHERE owner_id = :owner_id'),
        {'owner_id': owner_id}
    )
    return result.mappings().all()


async def get_todo_by_id(db: AsyncSession, todo_id: int, owner_id: int):
    result = await db.execute(
        text('SELECT * FROM todos WHERE id = :id AND owner_id = :owner_id'),
        {
            'id': todo_id,
            'owner_id': owner_id,
        }
    )
    return result.mappings().fetchone()


async def create_todo(db: AsyncSession, todo_request: TodosRequest, owner_id: int):
    todo_model = Todos(**todo_request.model_dump(), owner_id=owner_id)
    db.add(todo_model)
    await db.commit()


async def update_todo(db: AsyncSession, todo_id: int, todo_request: TodosRequest, owner_id: int):
    todo_model = todo_request.model_dump()
    await db.execute(
        text('''
            UPDATE todos
               SET title = :title,
                   description = :description,
                   priority = :priority,
                   complete = :complete
             WHERE id = :todo_id
               AND owner_id = :owner_id
        '''),
        {
            'todo_id': todo_id,
            'owner_id': owner_id,
            'title': todo_model['title'],
            'description': todo_model['description'],
            'priority': todo_model['priority'],
            'complete': todo_model['complete']
        }
    )
    await db.commit()


async def delete_todo(db: AsyncSession, todo_id: int, owner_id: int):
    await db.execute(
        text('DELETE FROM todos WHERE id = :id AND owner_id = :owner_id'),
        {
            'id': todo_id,
            'owner_id': owner_id,
        }
    )
    await db.commit()
