from fastapi import APIRouter, HTTPException, Depends
from models.NotificationModel import NotificationModel, CreateNotificationModel
from pydantic_mongo.fields import ObjectIdField
from .auth import get_current_user
from models.UserModel import UserModel
from typing import List
from db.mongodb import MongoDB

router = APIRouter(prefix='/notifications', tags=['Notifications'])


@router.get('/', response_model=List[NotificationModel])
async def get_all_notifications(current_user: UserModel = Depends(get_current_user)):
    database = await MongoDB.get_db()
    database = database['notifications']
    notifications: list[NotificationModel] = []
    async for notification in database.find({'recipient': current_user['_id']}):
        notifications.append(notification)
    if notifications:
        return notifications
    raise HTTPException(status_code=404, detail='No notifications found')


@router.get('/{notification_id}', response_model=NotificationModel)
async def get_notification(notification_id: ObjectIdField):
    database = await MongoDB.get_db()
    database = database['notifications']
    res = await database.find_one({'_id': notification_id})
    if res:
        return res
    raise HTTPException(status_code=404, detail='Notification not found')


async def create_notification(notification: CreateNotificationModel):
    database = await MongoDB.get_db()
    database = database['notifications']
    result = await database.insert_one(notification.model_dump())
    new_notification = await database.find_one({'_id': result.inserted_id})
    return new_notification


@router.put('/{notification_id}', response_model=NotificationModel)
async def update_notification(notification_id: ObjectIdField, notification: NotificationModel):
    database = await MongoDB.get_db()
    database = database['notifications']
    result = await database.replace_one({'_id': notification_id}, notification.model_dump())
    if result:
        updated_notification = await database.find_one({'_id': notification_id})
        return updated_notification
    raise HTTPException(status_code=404, detail='Notification not found')


@router.delete('/{notification_id}')
async def delete_notification(notification_id: ObjectIdField):
    database = await MongoDB.get_db()
    database = database['notifications']
    result = await database.find_one({'_id': notification_id})
    if result:
        await database.delete_one({'_id': notification_id})
        return {'notification': 'Notification deleted successfully'}
    raise HTTPException(status_code=404, detail='Notification not found')
