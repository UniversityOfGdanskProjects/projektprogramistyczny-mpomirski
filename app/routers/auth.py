from datetime import timedelta, datetime, timezone
import re
from fastapi import APIRouter, FastAPI, HTTPException, Depends, Response, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from models.UserModel import UserModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from typing import Annotated
from jose import JWTError, jwt
from db.mongodb import MongoDB

router = APIRouter(prefix='/auth', tags=['Auth'])
SECRET_KEY = 'secret'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


class Token(BaseModel):
    access_token: str
    access_type: str


class TokenData(BaseModel):
    username: str | None = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    database = await MongoDB.get_db()
    database = database['users']
    find_user = await database.find_one({'username': username})
    if not find_user:
        return False
    if not verify_password(password, find_user['password']):
        return False
    return find_user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    database = await MongoDB.get_db()
    database = database['users']
    user = await database.find_one({'username': token_data.username})
    if user is None:
        raise credentials_exception
    return user


@router.post('/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires)
    return Token(access_token=access_token, access_type='bearer')


@router.get('/me', response_model=UserModel)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


@router.get('/logout')
async def logout(current_user: UserModel = Depends(get_current_user)):
    return RedirectResponse(url='/auth/login', status_code=302)
