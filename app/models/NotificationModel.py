from pydantic import BaseModel, Field
from pydantic_mongo.fields import ObjectIdField
from datetime import datetime
from bson import Binary


class NotificationModel(BaseModel):
    id: ObjectIdField = Field(alias='_id')
    recipient: ObjectIdField
    text: str
    timestamp: datetime
    read: bool = False


class CreateNotificationModel(BaseModel):
    recipient: ObjectIdField
    text: str
    timestamp: datetime = Field(default_factory=datetime.now)
    read: bool = False
