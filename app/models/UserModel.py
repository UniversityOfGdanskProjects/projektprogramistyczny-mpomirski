from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from pydantic_mongo.fields import ObjectIdField


class UserModel(BaseModel):
    id: ObjectIdField | str = Field(alias='_id')
    username: str
    email: EmailStr
    password: str
    registration_date: datetime
    channels: list[ObjectIdField] | list[str] = Field(default_factory=list)
    calls: list[ObjectIdField] | list[str] = Field(default_factory=list)


class CreateUserModel(BaseModel):
    username: str
    email: EmailStr
    password: str
    registration_date: datetime = Field(default_factory=datetime.now)
