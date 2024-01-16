from fastapi import APIRouter, HTTPException
from models.UserModel import UserModel, CreateUserModel
from pydantic_mongo.fields import ObjectIdField
from typing import List
from db.mongodb import MongoDB

router = APIRouter()


@router.get('/users', response_model=List[UserModel])
async def get_all_users():
    database = await MongoDB.get_db()
    database = database['users']
    users: list[UserModel] = []
    async for user in database.find():
        users.append(user)
    if users:
        return users
    raise HTTPException(status_code=404, detail='No users found')


@router.get('/users/{user_id}', response_model=UserModel)
async def get_user(user_id: ObjectIdField):
    database = await MongoDB.get_db()
    database = database['users']
    res = await database.find_one({'_id': user_id})
    if res:
        return res
    raise HTTPException(status_code=404, detail='User not found')


@router.post('/users', response_model=UserModel)
async def create_user(user: CreateUserModel):
    database = await MongoDB.get_db()
    database = database['users']
    try:
        result = await database.insert_one(user.model_dump())
    except Exception as e:
        raise HTTPException(
            status_code=400, detail="User with this email already exists")
    new_user = await database.find_one({'_id': result.inserted_id})
    return new_user


@router.put('/users/{user_id}', response_model=UserModel)
async def update_user(user_id: ObjectIdField, user: UserModel):
    database = await MongoDB.get_db()
    database = database['users']
    result = await database.replace_one({'_id': user_id}, user.model_dump())
    if result:
        updated_user = await database.find_one({'_id': user_id})
        return updated_user
    raise HTTPException(status_code=404, detail='User not found')


@router.delete('/users/{user_id}')
async def delete_user(user_id: ObjectIdField):
    database = await MongoDB.get_db()
    database = database['users']
    result = await database.find_one({'_id': user_id})
    if result:
        await database.delete_one({'_id': user_id})
        return {'message': 'User deleted successfully'}
    raise HTTPException(status_code=404, detail='User not found')
