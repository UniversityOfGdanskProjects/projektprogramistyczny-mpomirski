from fastapi import APIRouter, HTTPException
from models.ScreenshareModel import ScreenshareModel, CreateScreenshareModel
from pydantic_mongo.fields import ObjectIdField
from typing import List
from db.mongodb import MongoDB

router = APIRouter(prefix='/screenshares', tags=['Screenshares'])


@router.get('/', response_model=List[ScreenshareModel])
async def get_all_screenshares():
    database = await MongoDB.get_db()
    database = database['screenshares']
    screenshares: list[ScreenshareModel] = []
    async for screenshare in database.find():
        screenshares.append(screenshare)
    if screenshares:
        return screenshares
    raise HTTPException(status_code=404, detail='No screenshares found')


@router.get('/{screenshare_id}', response_model=ScreenshareModel)
async def get_screenshare(screenshare_id: ObjectIdField):
    database = await MongoDB.get_db()
    database = database['screenshares']
    res = await database.find_one({'_id': screenshare_id})
    if res:
        return res
    raise HTTPException(status_code=404, detail='Screenshare not found')


@router.post('/', response_model=ScreenshareModel)
async def create_screenshare(screenshare: CreateScreenshareModel):
    database = await MongoDB.get_db()
    database = database['screenshares']
    result = await database.insert_one(screenshare.model_dump())
    new_screenshare = await database.find_one({'_id': result.inserted_id})
    return new_screenshare


@router.put('/{screenshare_id}', response_model=ScreenshareModel)
async def update_screenshare(screenshare_id: ObjectIdField, screenshare: ScreenshareModel):
    database = await MongoDB.get_db()
    database = database['screenshares']
    result = await database.replace_one({'_id': screenshare_id}, screenshare.model_dump())
    if result:
        updated_screenshare = await database.find_one({'_id': screenshare_id})
        return updated_screenshare
    raise HTTPException(status_code=404, detail='Screenshare not found')


@router.delete('/{screenshare_id}')
async def delete_screenshare(screenshare_id: ObjectIdField):
    database = await MongoDB.get_db()
    database = database['screenshares']
    result = await database.find_one({'_id': screenshare_id})
    if result:
        await database.delete_one({'_id': screenshare_id})
        return {'message': 'Screenshare deleted successfully'}
    raise HTTPException(status_code=404, detail='Screenshare not found')
