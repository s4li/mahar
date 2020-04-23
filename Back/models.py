from sqlalchemy import Column, Table, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base #class stores a catlog of classes and mapped tables in the Declarative system
from sqlalchemy.orm import sessionmaker
import pymysql

user = 'root'
password = 'Salam159'
engine = create_engine(f'mysql+pymysql://{user}:{password}@localhost/mahar?charset=utf8') # Create the database in memory
Base = declarative_base() #function is used to create base class
Session = sessionmaker(bind = engine) # A session object is the handle to database
session = Session()

class User(Base):
   __tablename__ = 'tbl_user'
   id = Column(Integer, primary_key=True)
   full_name = Column(String)
   mobile = Column(String)
   password = Column(String)
   
