from pydantic import BaseModel, Field
from pydantic_mongo.fields import ObjectIdField


class ChannelModel(BaseModel):
    id: ObjectIdField | str = Field(alias='_id')
    channel_name: str
    owner: ObjectIdField | str
    members: list[ObjectIdField] | list[str] = Field(default_factory=list)
    messages: list[ObjectIdField] | list[str] = Field(default_factory=list)


class CreateChannelModel(BaseModel):
    channel_name: str
    owner: ObjectIdField | str
    members: list[ObjectIdField] | list[str] = Field(default_factory=list)
    messages: list[ObjectIdField] | list[str] = Field(default_factory=list)
