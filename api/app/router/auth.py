from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from datetime import timedelta, datetime, timezone
import jwt

from app.db.session import get_db
from app.services import auth
from app.schemas.auth import CreateUserRequest, Token
from app.utils.hash import Hash
from app.core.config import settings


router = APIRouter()

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

db_dependency = Annotated[AsyncSession, Depends(get_db)]
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest, db: db_dependency):
    '''Create a new user '''
    await auth.create_user(request=create_user_request, db=db)


def create_access_token(username: str, user_id: int, role: str, token_version: int, expires_delta: timedelta):
    encode = {
        'sub': username,
        'id': user_id,
        'role': role,
        'token_version': token_version
    }
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db: db_dependency):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY,
                             algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        user_role: str = payload.get('role')
        token_version: int = payload.get('token_version')
        if username is None or user_id is None:
            raise credentials_exception

        user = await auth.get_user_by_username(username, db)
        if user is None or user.token_version != token_version:
            raise credentials_exception

        return {'username': username, 'id': user_id, 'role': user_role}
    except jwt.PyJWTError:
        raise credentials_exception


@router.post('/token', response_model=Token)
async def authenticate_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    '''Return Access token'''
    user = await auth.get_user_by_username(form_data.username, db)

    if not user or not Hash.verify(user.hashed_password, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        'access_token': create_access_token(user.username, user.id, user.role, user.token_version, timedelta(minutes=20)),
        'token_type': 'bearer'
    }
