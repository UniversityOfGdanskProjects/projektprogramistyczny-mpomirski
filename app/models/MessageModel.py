from pydantic import BaseModel, Field
from pydantic_mongo.fields import ObjectIdField
from datetime import datetime


class MessageModel(BaseModel):
    id: ObjectIdField | str = Field(alias='_id')
    author: ObjectIdField | str
    text: str
    timestamp: datetime
    files: list[ObjectIdField] | list[str] = Field(default_factory=list)


class CreateMessageModel(BaseModel):
    author: ObjectIdField | str
    text: str
    timestamp: datetime = Field(default_factory=datetime.now)
    files: list[ObjectIdField] | list[str] = Field(default_factory=list)
