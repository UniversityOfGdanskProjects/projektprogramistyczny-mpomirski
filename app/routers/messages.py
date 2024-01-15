from fastapi import APIRouter, HTTPException
from models.MessageModel import MessageModel, CreateMessageModel
from pydantic_mongo.fields import ObjectIdField
from typing import List
from db.mongodb import MongoDB

router = APIRouter()


@router.get('/messages', response_model=List[MessageModel])
async def get_all_messages():
    messages_col = await MongoDB.get_db()
    messages_col = messages_col['messages']
    messages: list[MessageModel] = []
    async for message in messages_col.find():
        messages.append(message)
    if messages:
        return messages
    raise HTTPException(status_code=404, detail='No messages found')


@router.get('/messages/{message_id}', response_model=MessageModel)
async def get_message(message_id: ObjectIdField):
    messages_col = await MongoDB.get_db()
    messages_col = messages_col['messages']
    res = await messages_col.find_one({'_id': message_id})
    if res:
        return res
    raise HTTPException(status_code=404, detail='Message not found')


@router.post('/messages', response_model=MessageModel)
async def create_message(message: CreateMessageModel):
    messages_col = await MongoDB.get_db()
    messages_col = messages_col['messages']
    result = await messages_col.insert_one(message.model_dump())
    new_message = await messages_col.find_one({'_id': result.inserted_id})
    return new_message


@router.put('/messages/{message_id}', response_model=MessageModel)
async def update_message(message_id: ObjectIdField, message: MessageModel):
    messages_col = await MongoDB.get_db()
    messages_col = messages_col['messages']
    result = await messages_col.replace_one({'_id': message_id}, message.model_dump())
    if result:
        updated_message = await messages_col.find_one({'_id': message_id})
        return updated_message
    raise HTTPException(status_code=404, detail='Message not found')


@router.delete('/messages/{message_id}')
async def delete_message(message_id: ObjectIdField):
    messages_col = await MongoDB.get_db()
    messages_col = messages_col['messages']
    result = await messages_col.find_one({'_id': message_id})
    if result:
        await messages_col.delete_one({'_id': message_id})
        return {'message': 'Message deleted successfully'}
    raise HTTPException(status_code=404, detail='Message not found')
