from fastapi import APIRouter, HTTPException
from models.FileModel import FileModel, CreateFileModel
from pydantic_mongo.fields import ObjectIdField
from typing import List
from db.mongodb import MongoDB

router = APIRouter(prefix='/files', tags=['Files'])


@router.get('/', response_model=List[FileModel])
async def get_all_files():
    database = await MongoDB.get_db()
    database = database['files']
    files: list[FileModel] = []
    async for file in database.find():
        files.append(file)
    if files:
        return files
    raise HTTPException(status_code=404, detail='No files found')


@router.get('/{file_id}', response_model=FileModel)
async def get_file(file_id: ObjectIdField):
    database = await MongoDB.get_db()
    database = database['files']
    res = await database.find_one({'_id': file_id})
    if res:
        return res
    raise HTTPException(status_code=404, detail='File not found')


@router.post('/', response_model=FileModel)
async def create_file(file: CreateFileModel):
    database = await MongoDB.get_db()
    database = database['files']
    result = await database.insert_one(file.model_dump())
    new_file = await database.find_one({'_id': result.inserted_id})
    return new_file


@router.delete('/{file_id}')
async def delete_file(file_id: ObjectIdField):
    database = await MongoDB.get_db()
    database = database['files']
    result = await database.find_one({'_id': file_id})
    if result:
        await database.delete_one({'_id': file_id})
        return {'message': 'File deleted successfully'}
    raise HTTPException(status_code=404, detail='File not found')
