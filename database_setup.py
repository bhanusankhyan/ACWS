from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
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
    id = Column(Integer, autoincrement= 10, primary_key=True)
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
    basic = Column(Integer, nullable = False)
    standard = Column(Integer, nullable = False)
    comprehensive = Column(Integer, nullable = False)

engine = create_engine('postgresql+psycopg2://bhanu:bhanu@localhost/experiment6')
Base.metadata.create_all(engine)
