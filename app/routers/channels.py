from fastapi import APIRouter, HTTPException
from models.ChannelModel import ChannelModel, CreateChannelModel
from pydantic_mongo.fields import ObjectIdField
from typing import List
from db.mongodb import MongoDB

router = APIRouter()


@router.get('/channels', response_model=List[ChannelModel])
async def get_all_channels():
    channels_col = await MongoDB.get_db()
    channels_col = channels_col['channels']
    channels: list[ChannelModel] = []
    async for channel in channels_col.find():
        channels.append(channel)
    if channels:
        return channels
    raise HTTPException(status_code=404, detail='No channels found')


@router.get('/channels/{channel_id}', response_model=ChannelModel)
async def get_channel(channel_id: ObjectIdField):
    channels_col = await MongoDB.get_db()
    channels_col = channels_col['channels']
    res = await channels_col.find_one({'_id': channel_id})
    if res:
        return res
    raise HTTPException(status_code=404, detail='Channel not found')


@router.post('/channels', response_model=ChannelModel)
async def create_channel(channel: CreateChannelModel):
    channels_col = await MongoDB.get_db()
    channels_col = channels_col['channels']
    result = await channels_col.insert_one(channel.model_dump())
    new_channel = await channels_col.find_one({'_id': result.inserted_id})
    return new_channel


@router.put('/channels/{channel_id}', response_model=ChannelModel)
async def update_channel(channel_id: ObjectIdField, channel: ChannelModel):
    channels_col = await MongoDB.get_db()
    channels_col = channels_col['channels']
    result = await channels_col.replace_one({'_id': channel_id}, channel.model_dump())
    if result:
        updated_channel = await channels_col.find_one({'_id': channel_id})
        return updated_channel
    raise HTTPException(status_code=404, detail='Channel not found')


@router.delete('/channels/{channel_id}')
async def delete_channel(channel_id: ObjectIdField):
    channels_col = await MongoDB.get_db()
    channels_col = channels_col['channels']
    result = await channels_col.find_one({'_id': channel_id})
    if result:
        await channels_col.delete_one({'_id': channel_id})
        return {'message': 'Channel deleted successfully'}
    raise HTTPException(status_code=404, detail='Channel not found')
