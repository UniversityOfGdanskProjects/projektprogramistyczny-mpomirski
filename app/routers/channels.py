from fastapi import APIRouter, HTTPException
from models.ChannelModel import ChannelModel, CreateChannelModel
from pydantic_mongo.fields import ObjectIdField
from typing import List
from db.mongodb import MongoDB

router = APIRouter(prefix='/channels', tags=['Channels'])


@router.get('/', response_model=List[ChannelModel])
async def get_all_channels():
    database = await MongoDB.get_db()
    database = database['channels']
    channels: list[ChannelModel] = []
    async for channel in database.find():
        channels.append(channel)
    if channels:
        return channels
    raise HTTPException(status_code=404, detail='No channels found')


@router.get('/{channel_id}', response_model=ChannelModel)
async def get_channel(channel_id: ObjectIdField):
    database = await MongoDB.get_db()
    database = database['channels']
    res = await database.find_one({'_id': channel_id})
    if res:
        return res
    raise HTTPException(status_code=404, detail='Channel not found')


@router.post('/', response_model=ChannelModel)
async def create_channel(channel: CreateChannelModel):
    database = await MongoDB.get_db()
    database = database['channels']
    result = await database.insert_one(channel.model_dump())
    new_channel = await database.find_one({'_id': result.inserted_id})
    return new_channel


@router.put('/{channel_id}', response_model=ChannelModel)
async def update_channel(channel_id: ObjectIdField, channel: ChannelModel):
    database = await MongoDB.get_db()
    database = database['channels']
    result = await database.replace_one({'_id': channel_id}, channel.model_dump())
    if result:
        updated_channel = await database.find_one({'_id': channel_id})
        return updated_channel
    raise HTTPException(status_code=404, detail='Channel not found')


@router.delete('/{channel_id}')
async def delete_channel(channel_id: ObjectIdField):
    database = await MongoDB.get_db()
    database = database['channels']
    result = await database.find_one({'_id': channel_id})
    if result:
        await database.delete_one({'_id': channel_id})
        return {'message': 'Channel deleted successfully'}
    raise HTTPException(status_code=404, detail='Channel not found')
