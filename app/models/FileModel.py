from pydantic import BaseModel, Field, Base64Bytes
from pydantic_mongo.fields import ObjectIdField
from datetime import datetime


class FileModel(BaseModel):
    id: ObjectIdField = Field(alias='_id')
    author: ObjectIdField
    file: Base64Bytes
    timestamp: datetime


class CreateFileModel(BaseModel):
    author: ObjectIdField
    file: Base64Bytes
    timestamp: datetime = Field(default_factory=datetime.now)
