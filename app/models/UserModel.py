from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from pydantic_mongo.fields import ObjectIdField


class UserModel(BaseModel):
    id: ObjectIdField = Field(alias='_id')
    username: str
    email: EmailStr
    password: str
    registration_date: datetime
    channels: list[ObjectIdField] = Field(default_factory=list)
    calls: list[ObjectIdField] = Field(default_factory=list)


class CreateUserModel(BaseModel):
    username: str
    email: EmailStr
    password: str
    registration_date: datetime = Field(default_factory=datetime.now)
