from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from utils.analytics import calculate_reservation_status, calculate_user_reservation_status, desk_usage_analysis, get_reservation_count_by_date, get_top_desk_reservations, get_total_reservations, most_common_equipment as mostEquipement, peak_hours_analysis

analyticsRouter = APIRouter()


@analyticsRouter.get("/analyseNotificationService/analytics/peak-hours")
async def get_peak_hours():
   with get_db() as db: 
    return peak_hours_analysis(db)


@analyticsRouter.get("/analyseNotificationService/analytics/desk-usage")
async def get_desk_usage():
   with get_db() as db: 
    return desk_usage_analysis(db)
@analyticsRouter.get("/analyseNotificationService/analytics/reservation-by-date")
async def get_reservation_by_date():
   with get_db() as db: 
    return get_reservation_count_by_date (db)
   
# calculate_user_reservation_status
@analyticsRouter.get("/analyseNotificationService/analytics/office_remote_work")
async def office_remote_work():
   with get_db() as db: 
    return calculate_user_reservation_status (db)
# most_common_equipment

@analyticsRouter.get("/analyseNotificationService/analytics/most_common_equipment")
async def most_common_equipment ():
   with get_db() as db: 
    return mostEquipement (db)
   
# calculate_reservation_status
@analyticsRouter.get("/analyseNotificationService/analytics/reservations_status")
async def reservations_status ():
   with get_db() as db: 
    return calculate_reservation_status (db)