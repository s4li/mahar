from sqlalchemy import Column, Table, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base #class stores a catlog of classes and mapped tables in the Declarative system
from sqlalchemy.orm import sessionmaker, relationship
import pymysql
from .conection_info import password, user


engine = create_engine(f'mysql+pymysql://{user}:{password}@localhost/mahar?charset=utf8') # Create the database in memory
Base = declarative_base() #function is used to create base class
Session = sessionmaker(bind = engine) # A session object is the handle to database


class User(Base):
   __tablename__ = 'tbl_users'
   id = Column(Integer, primary_key=True)
   full_name = Column(String)
   mobile = Column(String)
   password = Column(String)
   purchased_lessons = Column(String,  default='1,9,16')
   user_answer = relationship('User_answer') 
   invoice = relationship('Invoice')  

class Course(Base):
   __tablename__ = 'tbl_courses'
   id = Column(Integer, primary_key=True)  
   title = Column(String)
   lesson = relationship('Lesson')

class Lesson(Base):
   __tablename__ = 'tbl_lessons'
   id = Column(Integer, primary_key=True)  
   title = Column(String)
   course_id = Column(Integer,ForeignKey('tbl_courses.id', ondelete='CASCADE'))
   voice = relationship('Voice') 
   question = relationship('Question') 
   user_answer = relationship('User_answer') 

class Voice(Base):
   __tablename__ = 'tbl_voices'
   id = Column(Integer, primary_key=True)  
   title = Column(String)
   path = Column(String)
   lesson_id = Column(Integer,ForeignKey('tbl_lessons.id', ondelete='CASCADE'))
   question = relationship('Question') 
   

class Question(Base):
   __tablename__ = 'tbl_questions'
   id = Column(Integer, primary_key=True)  
   text = Column(String)
   lesson_id = Column(Integer,ForeignKey('tbl_lessons.id', ondelete='CASCADE'))
   voice_id = Column(Integer,ForeignKey('tbl_voices.id', ondelete='CASCADE'))
   question = relationship('User_answer')
   answer = relationship('Answer') 

class Answer(Base):
   __tablename__ = 'tbl_answers'
   id = Column(Integer, primary_key=True)  
   ans_text = Column(String)
   check_ans = Column(String)
   question_id = Column(Integer,ForeignKey('tbl_questions.id', ondelete='CASCADE'))
   

class User_answer(Base):
   __tablename__ = 'tbl_user_answers'
   id = Column(Integer, primary_key=True)  
   ans_no = Column(String)
   user_id = Column(Integer,ForeignKey('tbl_users.id', ondelete='CASCADE'))
   question_id = Column(Integer,ForeignKey('tbl_questions.id', ondelete='CASCADE'))
   lesson_id = Column(Integer,ForeignKey('tbl_lessons.id', ondelete='CASCADE'))
   

class Sale_plan(Base):
   __tablename__ = 'tbl_sale_plan'
   id = Column(Integer, primary_key=True)  
   title = Column(String)
   price = Column(String)
   lessons = Column(String)
   invoice = relationship('Invoice') 

class Invoice(Base):
   __tablename__ = 'tbl_invoices'
   id = Column(Integer, primary_key=True)  
   invoice_no = Column(String)
   datetime = Column(String)
   transaction_reference_id = Column(String)
   status = Column(String)
   lessons = Column(String)
   user_id = Column(Integer,ForeignKey('tbl_users.id', ondelete='CASCADE'))
   sale_plan_id = Column(Integer,ForeignKey('tbl_sale_plan.id', ondelete='CASCADE'))



     



