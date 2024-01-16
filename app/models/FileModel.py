from pydantic import BaseModel, Field, Base64Bytes
from pydantic_mongo.fields import ObjectIdField
from datetime import datetime


class FileModel(BaseModel):
    id: ObjectIdField | str = Field(alias='_id')
    author: ObjectIdField | str
    file: Base64Bytes
    timestamp: datetime


class CreateFileModel(BaseModel):
    author: ObjectIdField | str
    file: Base64Bytes
    timestamp: datetime = Field(default_factory=datetime.now)
