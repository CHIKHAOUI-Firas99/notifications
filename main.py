from datetime import datetime
from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from database.database import Base,engine
from controllers.sendMail import send_email
from models.Demands import Demand
from models.Workspace import Workspace

from models.User import User

from models.Desk import Desk

from models.Material import Material
from models.DeskMaterial import DeskMaterial
from models.Notification import Notification
from routers.notificationRouter import notificationRouter
from routers.analyticsRouter import analyticsRouter
from sqlalchemy.orm import Session
from database.database import get_db

import pandas as pd 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
def reminder():
    with get_db() as db:
        list_users = db.query(User).all()
        notif_date = datetime.utcnow()

        for user in list_users:
                db.add(Notification(
                user_id=user.id,
                description='Book your reservation for next week as soon as possible to avoid delays.',
                title="Work slot reservation reminder",
                read=False,
                time=notif_date))
                db.commit()
                text="Dear "+user.name+",\nJust a quick reminder that all workers must book their work slot reservation before coming to work.\nPlease book your reservation for the upcoming week as soon as possible to avoid any delays.\nThank you for your cooperation.\nBest regards,Sheidt Bachman"
                send_email(user.email, subject='Work slot reservation reminder', body=text)
scheduler = BackgroundScheduler()

@scheduler.scheduled_job(trigger=CronTrigger(day_of_week='sun', hour=00,minute=16))
def my_task():
     
     reminder()
     
    
 
scheduler.start()

app.include_router(notificationRouter)
app.include_router(analyticsRouter)

# @app.get("/dataframe")
# async def get_data():
#     with get_db() as db:
#         data = pd.read_sql("SELECT * FROM users", con=db.bind)
#         return {"data": data.to_dict(orient="records")}
# @app.get("/peak-hour/")
# def get_peak_hour():
#     with get_db() as db:
#         df_reservations = pd.read_sql(db.query(Reservation).statement, db.bind)
#         df_reservations['hour'] = df_reservations['start_time'].dt.floor('H')
#         reservations_by_hour = df_reservations.groupby('hour').size().reset_index(name='num_reservations')
#         reservations_by_hour = reservations_by_hour.sort_values(by='num_reservations', ascending=False)
#         peak_hour = reservations_by_hour.iloc[0]['hour']
#         return {"peak_hour": peak_hour}

# Function to get equipment usage statistics
# @app.get("/equipment-usage/")
# def get_equipment_usage(db: Session = Depends(get_db)):
#     with db:
#         materials = db.query(Material).all()
#         usage_stats = {}
#         for material in materials:
#             usage_stats[material.name] = db.query(Reservation).join(Material).filter(Material.id == material.id).count()
#         return usage_stats