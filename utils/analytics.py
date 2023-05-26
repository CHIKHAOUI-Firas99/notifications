from typing import List, Tuple
import pandas as pd
from sqlalchemy import func
from sqlalchemy.orm import Session
from database.database import get_db
from models.Desk import Desk
from models.Material import Material
from models.Reservation import Reservation


from typing import List, Dict
from sqlalchemy.orm import Session
import pandas as pd
from datetime import timedelta, datetime as dt
import datetime

from datetime import timedelta, datetime as dt
import datetime

from models.User import User
def peak_hours_analysis(db: Session) -> List[Dict[str, str]]:
    today = dt.now().date()
    current_weekday = today.weekday()
    previous_monday = today - timedelta(days=current_weekday + 7)
    previous_friday = previous_monday + timedelta(days=4)
    print(previous_monday)
    print(previous_friday)
    reservations = db.query(Reservation.start_time, Reservation.end_time).filter(
            Reservation.date >= previous_monday,
            Reservation.date <= previous_friday,
            Reservation.status == "Passed"
        ).all()
    
    if not reservations:
            return []  # Return an empty list if there are no matching reservations
    else :
        df = pd.DataFrame(reservations, columns=['start_time', 'end_time'])
        print(df)
        df['start_time'] = pd.to_datetime(df['start_time'], format='%H:%M')
        df['end_time'] = pd.to_datetime(df['end_time'], format='%H:%M')

        df['period'] = df['start_time'].dt.strftime('%H:%M') + '-' + df['end_time'].dt.strftime('%H:%M')
        period_counts = df['period'].value_counts(normalize=True)

        peak_periods = period_counts.head(5).reset_index().rename(columns={'index': 'period', 'period': 'percentage'})
        peak_periods = peak_periods.assign(start_time=df['start_time'], end_time=df['end_time'])

        total_reservations = len(reservations)

        output_list = []
        for _, row in peak_periods.iterrows():
            print(row)
            period = row['percentage']
            occurrence = round(row['proportion'] * 100)

            output_list.append({
                'name': period,
                'value':str(occurrence)+' %'
            })

        return output_list
def desk_usage_analysis(db: Session) -> dict:
    reservations = db.query(Reservation.desk_id, Reservation.start_time, Reservation.end_time).filter(Reservation.status =='Passed').all()
    df = pd.DataFrame(reservations, columns=['desk_id', 'start_time', 'end_time'])
    df['duration'] = (pd.to_datetime(df['end_time']) - pd.to_datetime(df['start_time']))
    grouped_df = df.groupby('desk_id')['duration'].sum().reset_index()
    grouped_df['duration'] = (grouped_df['duration'].dt.seconds / 60).astype(int)
    if not isinstance(grouped_df.to_dict(orient='records'),list):
      return [{
          'name': 'desk '+ str(grouped_df.to_dict(orient='records')['desk_id']),
          'value': grouped_df.to_dict(orient='records')['duration'],

      }]
    else :
        l=list()
        for item in grouped_df.to_dict(orient='records'):
            l.append({
            'name': 'desk '+str(item['desk_id']),
          'value': item['duration'],
            })
         
        return l



def get_total_reservations(db: Session):
    try:
        total_reservations = db.query(func.count(Reservation.id)).scalar()
        return total_reservations
    except Exception as e:
        print(f"Error retrieving total reservations: {str(e)}")
        return None

from collections import OrderedDict

import calendar

import datetime

import datetime
import calendar

def get_reservation_count_by_date(db: Session):
    try:
        today = datetime.date.today()
        current_weekday = today.weekday()
        previous_monday = today - datetime.timedelta(days=current_weekday + 7)
        previous_friday = previous_monday + datetime.timedelta(days=4)

        reservation_data = db.query(Reservation.date).filter(
            Reservation.date >= previous_monday.strftime('%Y-%m-%d'),
            Reservation.date <= previous_friday.strftime('%Y-%m-%d'),
            Reservation.status == "Passed"
        ).all()

        if not reservation_data:
            return []  # Return an empty list if there are no matching reservations

        reservation_dates = [datetime.datetime.strptime(date_tuple[0], '%Y-%m-%d').date() for date_tuple in reservation_data]
        weekdays = [calendar.day_name[date.weekday()] for date in reservation_dates]

        df = pd.DataFrame({'weekday': weekdays})
        reservation_count_by_weekday = df.groupby('weekday').size().reset_index(name='count')
        total_reservations = reservation_count_by_weekday['count'].sum()
        reservation_count_by_weekday['percentage'] = reservation_count_by_weekday['count'] / total_reservations * 100

        # Define the order of weekdays
        order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        reservation_count_by_weekday['weekday'] = pd.Categorical(reservation_count_by_weekday['weekday'], categories=order, ordered=True)
        reservation_count_by_weekday = reservation_count_by_weekday.sort_values('weekday')

        result = [OrderedDict(row) for _, row in reservation_count_by_weekday[['weekday', 'percentage']].iterrows()]
        l = []
        for item in result:
            l.append({
                "name": item['weekday'],
                "value": item['percentage']
            })
        return l
    except Exception as e:
        print(f"Error retrieving reservation count by date: {str(e)}")
        return None



    
from sqlalchemy.orm import joinedload
from sqlalchemy import func

def most_common_equipment(db):
    desks = db.query(Desk).options(joinedload(Desk.desk_materials)).all()

    material_counts = {}
    total_desks = len(desks)

    for desk in desks:
        for material in desk.desk_materials:
            material_counts[material.material_id] = material_counts.get(material.material_id, 0) + 1

    material_usage_list = []
    for material_id, count in material_counts.items():
        material = db.query(Material).filter(Material.id == material_id).first()
        if material:
            percentage = round(count / total_desks * 100, 2)
            material_usage_list.append({
                'name': material.name,
                'value': percentage
            })

    return material_usage_list















def get_top_desk_reservations(db: Session):
    try:
        reservation_data = db.query(Reservation.desk_id).all()
        df = pd.DataFrame(reservation_data, columns=['desk_id'])
        top_desk_reservations = df['desk_id'].value_counts().reset_index().rename(columns={'index': 'desk_id', 'desk_id': 'count'})
        return top_desk_reservations.to_dict('records')
    except Exception as e:
        print(f"Error retrieving top desk reservations: {str(e)}")
        return None


def calculate_user_reservation_status(db: Session) -> Dict[str, int]:
    today = dt.now().date()
    current_weekday = today.weekday()
    previous_monday = today - timedelta(days=current_weekday + 7)
    previous_friday = previous_monday + timedelta(days=4)
    reservations = db.query(Reservation).filter(
            Reservation.date >= previous_monday,
            Reservation.date <= previous_friday,
            Reservation.status == "Passed"
        ).all()
    users = db.query(User).all()

    reservation_user_ids = [reservation.user_id for reservation in reservations]
    all_user_ids = [user.id for user in users]

    reservation_df = pd.DataFrame({'user_id': reservation_user_ids})
    user_df = pd.DataFrame({'user_id': all_user_ids})

    users_with_reservations = len(reservation_df['user_id'].unique())
    users_without_reservations = len(user_df[~user_df['user_id'].isin(reservation_df['user_id'])])
    l=list()
    l.append({
        "name": "Office",
        "value": users_with_reservations
    })
    l.append({
        "name": "Remote",
        "value": users_without_reservations
    })


    return l

def calculate_reservation_status(db: Session) -> Dict[str, int]:
    try:
        today = dt.now().date()
        current_weekday = today.weekday()
        previous_monday = today - timedelta(days=current_weekday + 7)
        previous_friday = previous_monday + timedelta(days=4)
        reservations = db.query(Reservation).filter(
            Reservation.date >= previous_monday,
            Reservation.date <= previous_friday,
            # Reservation.status == "Passed"
        ).all()
        df = pd.DataFrame([(reservation.status) for reservation in reservations], columns=['status'])
        reservation_counts = df['status'].value_counts(normalize=True) * 100

        result = []
        for status, percentage in reservation_counts.items():
            result.append({
                "name": status,
                "value": round(percentage, 2)
            })

        return result
    except Exception as e:
        print(f"Error calculating reservation status: {str(e)}")
        return None