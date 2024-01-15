from pydantic import BaseModel, Field
from pydantic_mongo.fields import ObjectIdField


class ChannelModel(BaseModel):
    id: ObjectIdField = Field(alias='_id')
    channel_name: str
    owner: ObjectIdField
    members: list[ObjectIdField] = Field(default_factory=list)
    messages: list[ObjectIdField] = Field(default_factory=list)


class CreateChannelModel(BaseModel):
    channel_name: str
    owner: ObjectIdField
    members: list[ObjectIdField] = Field(default_factory=list)
    messages: list[ObjectIdField] = Field(default_factory=list)
