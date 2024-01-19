from pydantic import BaseModel, Field
from pydantic_mongo.fields import ObjectIdField
from datetime import datetime


class NotificationModel(BaseModel):
    id: ObjectIdField | str = Field(alias='_id')
    recipient: ObjectIdField | str
    text: str
    timestamp: datetime
    read: bool = False


class CreateNotificationModel(BaseModel):
    recipient: ObjectIdField | str
    text: str
    timestamp: datetime = Field(default_factory=datetime.now)
    read: bool = False
