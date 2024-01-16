from pydantic import BaseModel, Field
from pydantic_mongo.fields import ObjectIdField
from datetime import datetime


class ScreenshareModel(BaseModel):
    id: ObjectIdField | str = Field(alias='_id')
    members: list[ObjectIdField] | list[str] = Field(default_factory=list)
    timestamp: datetime


class CreateScreenshareModel(BaseModel):
    members: list[ObjectIdField] | list[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)
