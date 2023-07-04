from database import sqlite
from sqlalchemy import cast, Date
from datetime import datetime, timedelta, date


def add_user(username, user_id):
    """Добавляет каждого нового пользователь через /start"""
    session = sqlite.Session()
    user_id = str(user_id)
    exists_user = session.query(sqlite.AllUser).filter_by(user_id=user_id).first()
    if exists_user:
        return
    
    new_user = sqlite.AllUser(username=username, user_id=user_id)
    session.add(new_user)
    session.commit()     


def add_price(service, price):
    """Добавление цен."""
    session = sqlite.Session()
    new_price = sqlite.Price(service=service, price=price)
    session.add(new_price)
    session.commit()

def delete_price(service):
    """Удаление цены."""
    session = sqlite.Session()
    prices = session.query(sqlite.Price).filter_by(service=service).all()
    for price in prices:
        session.delete(price)
    session.commit()

def get_prices():
    """Возвращает список всех цен из базы данных"""
    session = sqlite.Session()
    prices = session.query(sqlite.Price).all()
    return prices

def add_date_time(date, start_time, end_time):
    session = sqlite.Session()
    new_date_time = sqlite.WorkBrowsTime(weekday=date, start_time=start_time, end_time=end_time)
    session.add(new_date_time)
    session.commit()

def get_date_time():
    current_date = datetime.today().strftime('%d-%m-%Y')
    session = sqlite.Session()
    dates = session.query(sqlite.WorkBrowsTime).filter(cast(sqlite.WorkBrowsTime.weekday, Date) >= current_date).all()
    return dates

def date_time_del(date):
    session = sqlite.Session()
    date_time = session.query(sqlite.WorkBrowsTime).filter_by(weekday=date).first()
    session.delete(date_time)
    session.commit()

def date_time_del_none():
    session = sqlite.Session()
    empty_rows = session.query(sqlite.WorkBrowsTime).filter(sqlite.WorkBrowsTime.weekday == None).all()
    for row in empty_rows:
        session.delete(row)
    session.commit()

def date_to_time(date):
    session = sqlite.Session()
    work_schedule = session.query(sqlite.WorkBrowsTime).filter_by(weekday=date).first()
    if not work_schedule:
        return 'нет времени'

    start_time = datetime.strptime(work_schedule.start_time, '%H:%M')
    end_time = datetime.strptime(work_schedule.end_time, '%H:%M')
    time_slot = timedelta(minutes=90)
    appoiments = session.query(sqlite.AppointmentUser).filter_by(appointment_date=date).all()

    appoiments_slot = [
        start_time + i * time_slot for i in range((end_time - start_time) // time_slot)
    ]
    aviable_times = []

    for appoiment_time in appoiments_slot:
        appoiment_time_str = appoiment_time.strftime('%H:%M')
        if not any([appoiment_time_str == appoiment.appointment_time for appoiment in appoiments]):
            aviable_times.append(appoiment_time_str)
    return aviable_times

def enwork_client_add(name, service, price, date, time, client_user_id):
    session = sqlite.Session()
    client_user_id = str(client_user_id)
    new_enwork_client = sqlite.AppointmentUser(
        client_name=name, client_service=service, client_user_id=client_user_id, client_price=price, appointment_date=date, appointment_time=time
    )
    session.add(new_enwork_client)
    session.commit()

def get_enwork_client():
    session = sqlite.Session()
    client = session.query(sqlite.AppointmentUser).all()
    return client

def client_del(client_user_id):
    session = sqlite.Session()
    appointment_user = session.query(sqlite.AppointmentUser).filter_by(client_user_id=client_user_id).all()

    if appointment_user:
        for row in appointment_user:
            session.delete(row)
        session.commit()
    else:
        session.rollback()

def client_user_id(client_user_id):
    session = sqlite.Session()
    client = session.query(sqlite.AppointmentUser).filter_by(client_user_id=client_user_id).all()
    return client

def add_sale(sale):
    session = sqlite.Session()

    new_sale = sqlite.Sale(text=sale)
    session.add(new_sale)
    session.commit()

def del_sale():
    session = sqlite.Session()
    all_sale_delete = session.query(sqlite.Sale).delete()
    session.commit()

def get_sale():
    session = sqlite.Session()
    sale = session.query(sqlite.Sale).all()
    return sale