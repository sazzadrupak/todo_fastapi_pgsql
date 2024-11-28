from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


from app.router import auth, admin, user, todos
from app.db.session import engine, Base


origins = ['http://localhost:5173']


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the database tables (or handle migrations)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def health_check():
    '''Application's health check API'''
    return {'status': 'healthy'}


# app.include_router(blog_post.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(user.router)
app.include_router(todos.router)
