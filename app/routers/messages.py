from fastapi import APIRouter, HTTPException
from models.MessageModel import MessageModel, CreateMessageModel
from pydantic_mongo.fields import ObjectIdField
from typing import List
from db.mongodb import MongoDB

router = APIRouter(prefix='/messages', tags=['Messages'])


@router.get('/', response_model=List[MessageModel])
async def get_all_messages():
    database = await MongoDB.get_db()
    database = database['messages']
    messages: list[MessageModel] = []
    async for message in database.find():
        messages.append(message)
    if messages:
        return messages
    raise HTTPException(status_code=404, detail='No messages found')


@router.get('/{message_id}', response_model=MessageModel)
async def get_message(message_id: ObjectIdField):
    database = await MongoDB.get_db()
    database = database['messages']
    res = await database.find_one({'_id': message_id})
    if res:
        return res
    raise HTTPException(status_code=404, detail='Message not found')


@router.post('/', response_model=MessageModel)
async def create_message(message: CreateMessageModel):
    database = await MongoDB.get_db()
    database = database['messages']
    result = await database.insert_one(message.model_dump())
    new_message = await database.find_one({'_id': result.inserted_id})
    return new_message


@router.put('/{message_id}', response_model=MessageModel)
async def update_message(message_id: ObjectIdField, message: MessageModel):
    database = await MongoDB.get_db()
    database = database['messages']
    result = await database.replace_one({'_id': message_id}, message.model_dump())
    if result:
        updated_message = await database.find_one({'_id': message_id})
        return updated_message
    raise HTTPException(status_code=404, detail='Message not found')


@router.delete('/{message_id}')
async def delete_message(message_id: ObjectIdField):
    database = await MongoDB.get_db()
    database = database['messages']
    result = await database.find_one({'_id': message_id})
    if result:
        await database.delete_one({'_id': message_id})
        return {'message': 'Message deleted successfully'}
    raise HTTPException(status_code=404, detail='Message not found')
