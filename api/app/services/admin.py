from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi import HTTPException

from app.schemas.todos import TodosRequest
from app.models.todos import Todos


async def get_all_todos(db: AsyncSession):
    result = await db.execute(text('SELECT * FROM todos'))
    return result.mappings().all()


async def get_todo_by_id(db: AsyncSession, todo_id: int):
    result = await db.execute(
        text('SELECT * FROM todos WHERE id = :id'),
        {'id': todo_id}
    )
    return result.mappings().fetchone()


async def delete_todo(db: AsyncSession, todo_id: int):
    await db.execute(
        text('DELETE FROM todos WHERE id = :id'),
        {'id': todo_id}
    )
    await db.commit()
