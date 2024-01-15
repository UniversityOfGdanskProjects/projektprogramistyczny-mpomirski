from pydantic import BaseModel, Field
from pydantic_mongo.fields import ObjectIdField
from datetime import datetime


class CallModel(BaseModel):
    id: ObjectIdField = Field(alias='_id')
    members: list[ObjectIdField] = Field(default_factory=list)
    timestamp: datetime


class CreateCallModel(BaseModel):
    members: list[ObjectIdField] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)
