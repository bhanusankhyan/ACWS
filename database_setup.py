from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Time, BigInteger, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql.base import UUID
Base = declarative_base()
import uuid
from sqlalchemy.sql.functions import GenericFunction
from sqlalchemy_utils import UUIDType
from random import randint
import random
values = [0,1,2,3,4,5,6,7,8,9]
class Register(Base):
    __tablename__ = 'register'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable = False)
    phone = Column(BigInteger, nullable=False, unique=True)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(30), nullable=False)
    date =  Column(DateTime, server_default = func.now() )

    @property
    def serialize(self):
        return{
    'id'        : self.id,
    'email'     : self.email,
    'password'  : self.password,
    'date'      : self.date,
    }

class Companies(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key = True, autoincrement = 20)
    name = Column(String(20), nullable = False, unique = True)

class Models(Base):
    __tablename__  = 'models'
    id = Column(Integer, ForeignKey('companies.id'))
    model_id = Column(Integer, autoincrement = True)
    company_id = relationship(Companies)
    model = Column(String(20), nullable=False, unique = True, primary_key = True)
    basic = Column(Integer)
    standard = Column(Integer)
    comprehensive = Column(Integer)

    @property
    def serial(self):
      return{
           'model' : self.model,
           'basic' : self.basic,
           'standard' : self.standard,
           'comprehensive' : self.comprehensive,
  }

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, nullable=False, autoincrement = True, primary_key=True)
    user_id = Column(Integer, ForeignKey('register.id'))
    reigster = relationship(Register)
    model = Column(String(20),nullable=False)
    workshop_id = Column(Integer)
    company_id = Column(Integer, ForeignKey('companies.id'))
    companies = relationship(Companies)
    booking_type = Column(String(30),nullable= False)
    price = Column(Integer)
    booking_time = Column(DateTime, server_default = func.now())
    booking_date = Column(Date, nullable = False)
    time_slot1 = Column(Time, nullable=False)
    time_slot2 = Column(Time)

class Workshop(Base):
    __tablename__ = 'workshops'
    id = Column(Integer, primary_key = True, autoincrement = True)
    date = Column(DateTime, server_default = func.now())
    name = Column(String(40), nullable= False)
    email_address = Column(String(30), nullable=False, unique=True)
    phone_number = Column(BigInteger,nullable=False,unique=True)
    latitude = Column(String(40))
    longitude = Column(String(40))
    password = Column(String(30))
    aadhar_num = Column(BigInteger,nullable=False,unique=True)
    workshop_id = Column(String(30),unique=True, nullable=False)
    gst = Column(String(30),nullable = False, unique=True)



engine = create_engine('postgresql+psycopg2://bhanu:bhanu@localhost/mendax')
Base.metadata.create_all(engine)
