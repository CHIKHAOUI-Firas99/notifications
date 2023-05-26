from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from controllers.sendMail import send_emails

from models.Notification import Notification
from schemas.Emails import SendEmails


def get_notifications_by_user_id(db: Session, user_id: int):
    
    with db as session:
        notifications = session.query(Notification).filter(Notification.user_id == user_id,Notification.deleted==False).all()
        if not notifications:
            return []
        
    return notifications

def acceptNotification(user_id,des,db):
    notif_date = datetime.utcnow()
    
    with db as session:
        session.add(Notification(
            user_id=user_id,
            description=des,
            title="Material request",
            read=False,
            deleted=False,
            sender='SCHEIDT & BACHMAN',
            time=notif_date
        ))
        session.commit()
    
    return "Ok"


def refuseNotification(user_id,des,db):
        notif_date = datetime.utcnow()
        print('bwwwwwwwwwwwwww',des)
        with db as session:
            session.add(Notification(
                user_id=user_id,
                description=des,
                title="Material request",
                read=False,
                deleted=False,
            sender='SCHEIDT & BACHMAN'

                ,time=notif_date
            ))
            session.commit()
        return "Ok"

def delete_notification_by_id(db: Session, notification_id: int):
    with db as session:
        notification = session.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        notification.deleted=True
        session.commit()
    return notification
def markAsRead(notification_id: int,db:Session):
    with db as session:
        notification = session.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        notification.read=not notification.read
        session.commit()
    return notification

def markAsUnRead(notification_id: int,db:Session):
    with db as session:
        notification = session.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        notification.read=False
        session.commit()
    return notification


def markAllAsRead(db:Session):
    with db as session:
        notifications = session.query(Notification).all()
        for notification in notifications:
        
            notification.read=True
        session.commit()
    return "succedded"

def sendEmails(SendEmails:SendEmails):
    
    send_emails(SendEmails)
        
    return "succedded"
