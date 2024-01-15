from fastapi import APIRouter, HTTPException
from models.CallModel import CallModel, CreateCallModel
from pydantic_mongo.fields import ObjectIdField
from typing import List
from db.mongodb import MongoDB

router = APIRouter()


@router.get('/calls', response_model=List[CallModel])
async def get_all_calls():
    database = await MongoDB.get_db()
    database = database['calls']
    calls: list[CallModel] = []
    async for call in database.find():
        calls.append(call)
    if calls:
        return calls
    raise HTTPException(status_code=404, detail='No calls found')


@router.get('/calls/{call_id}', response_model=CallModel)
async def get_call(call_id: ObjectIdField):
    database = await MongoDB.get_db()
    database = database['calls']
    res = await database.find_one({'_id': call_id})
    if res:
        return res
    raise HTTPException(status_code=404, detail='Call not found')


@router.post('/calls', response_model=CallModel)
async def create_call(call: CreateCallModel):
    database = await MongoDB.get_db()
    database = database['calls']
    result = await database.insert_one(call.model_dump())
    new_call = await database.find_one({'_id': result.inserted_id})
    return new_call


@router.put('/calls/{call_id}', response_model=CallModel)
async def update_call(call_id: ObjectIdField, call: CallModel):
    database = await MongoDB.get_db()
    database = database['calls']
    result = await database.replace_one({'_id': call_id}, call.model_dump())
    if result:
        updated_call = await database.find_one({'_id': call_id})
        return updated_call
    raise HTTPException(status_code=404, detail='Call not found')


@router.delete('/calls/{call_id}')
async def delete_call(call_id: ObjectIdField):
    database = await MongoDB.get_db()
    database = database['calls']
    result = await database.find_one({'_id': call_id})
    if result:
        await database.delete_one({'_id': call_id})
        return {'message': 'Call deleted successfully'}
    raise HTTPException(status_code=404, detail='Call not found')
