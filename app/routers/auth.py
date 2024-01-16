from gettext import find
from fastapi import APIRouter, HTTPException, Response, Depends, Security

from pydantic_mongo.fields import ObjectIdField
from models.UserModel import CreateUserModel
from utils.security import hash_password, verify_password
from fastapi_jwt import JwtAccessBearerCookie, JwtAuthorizationCredentials, JwtRefreshBearer
from typing import List
from db.mongodb import MongoDB

router = APIRouter()

# change the secret key
access_security = JwtAccessBearerCookie(secret_key='secret', auto_error=True)
refresh_security = JwtRefreshBearer(secret_key='secret', auto_error=True)


@router.post('/auth/register', status_code=201)
async def register_user(user: CreateUserModel):
    database = await MongoDB.get_db()
    database = database['users']
    find_user = await database.find_one({'email': user.email})
    if find_user:
        raise HTTPException(status_code=409, detail='User already exists')
    user.password = hash_password(user.password)
    new_user = await database.insert_one(user.model_dump())
    if new_user:
        return user
    raise HTTPException(status_code=400, detail='User not created')


@router.post('/auth/login')
async def login_user(user: CreateUserModel, response: Response):
    database = await MongoDB.get_db()
    database = database['users']
    find_user = await database.find_one({'email': user.email})
    if not find_user:
        raise HTTPException(status_code=404, detail='User not found')
    if not verify_password(user.password, find_user['password']):
        raise HTTPException(
            status_code=401, detail='Invalid email or password')

    access_token = access_security.create_access_token(
        subject=({"_id": str(find_user['_id'])}))
    refresh_token = refresh_security.create_refresh_token(
        subject=({"_id": str(find_user['_id'])}))

    access_security.set_access_cookie(response, access_token)
    response.co()
    refresh_security.set_refresh_cookie(response, refresh_token)

    return {'status': 'success', 'access_token': access_token, 'refresh_token': refresh_token}


@router.get('/auth/logout')
async def logout_user(response: Response):
    access_security.unset_access_cookie(response)
    refresh_security.unset_refresh_cookie(response)
    return {'status': 'success', 'message': 'Logged out'}
