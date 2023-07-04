import sqlite3, os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Date 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PGUSER = 'postgres'
PGPASSWORD = 'Vorobev2005'
ip = 'localhost'
port = 5432
DATABASE = 'browws_polina'


Base = declarative_base()
engine = create_engine(f'postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}', echo=True)
Session = sessionmaker(bind=engine)


class AllUser(Base):
    __tablename__ = 'all_user'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    user_id = Column(String)

class Price(Base):
    __tablename__ = 'price'

    id = Column(Integer, primary_key=True)
    service = Column(String)
    price = Column(Integer)


class AppointmentUser(Base):
    __tablename__ = 'enworkbrowsuser'

    id = Column(Integer, primary_key=True)
    client_name = Column(String)
    client_service = Column(String)
    client_user_id = Column(String)
    client_price = Column(String)
    appointment_date = Column(String)
    appointment_time = Column(String)  
    sucsess = Column(String, default='False')

class WorkBrowsTime(Base):
    __tablename__ = "work_brows_time"

    id = Column(Integer, primary_key=True)
    weekday = Column(String)
    start_time = Column(String)
    end_time = Column(String)

class Sale(Base):
    __tablename__ = "sale"

    id = Column(Integer, primary_key=True)
    text = Column(String)    


Base.metadata.create_all(engine)
