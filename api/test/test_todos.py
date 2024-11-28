"""
Test cases for Todo APIs
"""


import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import text
from sqlalchemy.future import select


from app.models.todos import Todos
from app.db.session import Base, get_db
from app.main import app
from app.router.auth import get_current_user


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./testdb.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
    echo=True
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def init_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def override_get_db():
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

user_admin = {'username': 'sazzad.rupak', 'id': 1, 'role': 'admin'}
user_one = {'username': 'sazzad.rupak', 'id': 2, 'role': 'user'}


def override_get_current_user(user):
    """
    Returns a dependency override function that always returns the specified user.
    """
    def dependency_override():
        return user
    return dependency_override


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user(
    user_one)


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def setup_test_db():
    await init_test_db()


@pytest.fixture(scope="module")
async def test_todo():
    """
    Create the test database schema before any tests run,
    and drop it after all tests are done.
    """
    async with TestingSessionLocal() as db:
        try:
            yield db
        finally:
            await db.execute(text('DELETE FROM todos;'))
            await db.commit()
            await db.close()
    # async with TestingSessionLocal() as db:
    #     todo = Todos(
    #         title="A new book",
    #         description="A new description of a book",
    #         priority=5,
    #         complete=False,
    #         owner_id=1,
    #     )

    #     db.add(todo)
    #     await db.commit()
    #     yield todo

    #     print('*****DELETING TEST TODOS DATA******')
    #     await db.execute(text('DELETE FROM todos;'))
    #     await db.commit()


client = TestClient(app)


@pytest.mark.anyio
async def test_create_todo(test_todo):
    """
      Test create a new todo
    """
    request_data = {
        'title': 'New Todo!',
        'description': 'New todo description',
        'priority': 5,
        'complete': False
    }

    response = client.post('/todos', json=request_data)
    assert response.status_code == 201
    async with TestingSessionLocal() as db:
        result = await db.execute(select(Todos).where(Todos.id == 1))
        model = result.scalars().first()
        assert model is not None
        assert model.title == request_data.get('title')


# {'complete': False, 'title': "A new book", 'description': "A new description of a book", 'id': 1, 'priority': 5, 'owner_id': 1}
@pytest.mark.anyio
async def test_read_all_authenticated(test_todo):
    """
      Test list of todos for authenticated user
    """
    response = client.get('/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': "New Todo!",
                                'description': "New todo description", 'id': 1, 'priority': 5, 'owner_id': 2}]


@pytest.mark.anyio
async def test_read_one_authenticated(test_todo):
    """
      Test todo detail for authenticated user
    """
    response = client.get('/todos/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': False, 'title': "New Todo!",
                               'description': "New todo description", 'id': 1, 'priority': 5, 'owner_id': 2}


@pytest.mark.anyio
async def test_read_one_authenticated_not_found():
    """
      Test todo not found for authenticated user
    """
    response = client.get('/todos/99')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo item not found'}


@pytest.mark.anyio
async def test_user_can_not_see_other_users_todo_list(test_todo):
    """
      Test create a new todo
    """
    app.dependency_overrides[get_current_user] = override_get_current_user(
        user_admin)
    request_data = {
        'title': 'Another New Todo!',
        'description': 'Another New todo description',
        'priority': 5,
        'complete': False
    }

    app.dependency_overrides[get_current_user] = override_get_current_user(
        user_one)
    response = client.get('/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': "New Todo!",
                                'description': "New todo description", 'id': 1, 'priority': 5, 'owner_id': 2}]
