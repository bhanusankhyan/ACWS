from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func
Base = declarative_base()

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


engine = create_engine('postgresql+psycopg2://bhanu:bhanu@localhost/acws6')
Base.metadata.create_all(engine)
