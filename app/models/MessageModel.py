from pydantic import BaseModel, Field
from pydantic_mongo.fields import ObjectIdField
from datetime import datetime


class MessageModel(BaseModel):
    id: ObjectIdField = Field(alias='_id')
    author: ObjectIdField
    text: str
    timestamp: datetime


class CreateMessageModel(BaseModel):
    author: ObjectIdField
    text: str
    timestamp: datetime = Field(default_factory=datetime.now)
