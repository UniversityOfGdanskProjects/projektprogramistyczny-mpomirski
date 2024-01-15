from fastapi import FastAPI, HTTPException
import motor.motor_asyncio
import asyncio
from typing import List, Any
import os
import uvicorn
from models.UserModel import UserModel, CreateUserModel
from pydantic_mongo.fields import ObjectIdField

app = FastAPI()
MONGO_URI = os.environ['APP_URI']
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

db = client['discord-clone']
channels_col = db['channels']
messages_col = db['messages']
users_col = db['users']


async def main():
    try:
        await client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


@app.get('/users', response_model=List[UserModel])
async def get_all_users():
    users: list[UserModel] = []
    try:
        async for user in users_col.find():
            users.append(user)
        return users
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get('/users/{user_id}', response_model=UserModel)
async def get_user(user_id: ObjectIdField):
    try:
        res = await users_col.find_one({'_id': user_id})
        return res
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post('/users', response_model=UserModel)
async def create_user(user: CreateUserModel):
    result = await users_col.insert_one(user.model_dump())
    new_user = await users_col.find_one({'_id': result.inserted_id})
    return new_user


@app.put('/users/{user_id}', response_model=UserModel)
async def update_user(user_id: ObjectIdField, user: UserModel):
    result = await users_col.update_one({'_id': user_id}, {'$set': user.model_dump()})
    return result


@app.delete('/users/{user_id}')
async def delete_user(user_id: ObjectIdField):
    result = await users_col.find_one({'_id': user_id})
    if result:
        await users_col.delete_one({'_id': user_id})
        return {'message': 'User deleted successfully'}
    return {'message': 'User not found'}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


# TODO: Fix error when searching for non existant id, it returns a 500 error instead of a 404
# TODO: Add a way to add channels to a user
# TODO: Add channels and messages endpoints
