from sqlalchemy import Column, Table, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base #class stores a catlog of classes and mapped tables in the Declarative system
from sqlalchemy.orm import sessionmaker, relationship
import pymysql
from conection_info import mysql_password, mysql_user, host, db_name


engine = create_engine(f'mysql+pymysql://{mysql_user}:{mysql_password}@{host}/{db_name}?charset=utf8', pool_size=1, max_overflow=-1) # Create the database in memory
Base = declarative_base() #function is used to create base class
Session = sessionmaker(bind = engine) # A session object is the handle to database



class User(Base):
   __tablename__ = 'tbl_users'
   id = Column(Integer, primary_key=True)
   full_name = Column(String(100))
   mobile = Column(String(45))
   password = Column(String(200))
   purchased_lessons = Column(String(500), default='1,9,16,20,32,42')
   confirm_code = Column(String(45), default='0')
   grade = Column(String(45) , default='na')
   city = Column(String(45) , default='na')
   user_answer = relationship('User_answer') 
   invoice = relationship('Invoice')  
   enrol_user = relationship('Enrol_user') 

class Course(Base):
   __tablename__ = 'tbl_courses'
   id = Column(Integer, primary_key=True)  
   title = Column(String(45))
   lesson = relationship('Lesson')
   image = Column(String(45))

class Lesson(Base):
   __tablename__ = 'tbl_lessons'
   id = Column(Integer, primary_key=True)  
   title = Column(String(45))
   course_id = Column(Integer,ForeignKey('tbl_courses.id', ondelete='CASCADE'))
   voice = relationship('Voice') 
   question = relationship('Question') 
   user_answer = relationship('User_answer')
   enrol_user = relationship('Enrol_user') 

class Voice(Base):
   __tablename__ = 'tbl_voices'
   id = Column(Integer, primary_key=True)  
   title = Column(String(45))
   path = Column(String(100))
   lesson_id = Column(Integer,ForeignKey('tbl_lessons.id', ondelete='CASCADE'))
   question = relationship('Question') 
   

class Question(Base):
   __tablename__ = 'tbl_questions'
   id = Column(Integer, primary_key=True)  
   text = Column(String(45))
   lesson_id = Column(Integer,ForeignKey('tbl_lessons.id', ondelete='CASCADE'))
   voice_id = Column(Integer,ForeignKey('tbl_voices.id', ondelete='CASCADE'))
   question = relationship('User_answer')
   answer = relationship('Answer') 

class Answer(Base):
   __tablename__ = 'tbl_answers'
   id = Column(Integer, primary_key=True)  
   ans_text = Column(String(45))
   check_ans = Column(String(45))
   question_id = Column(Integer,ForeignKey('tbl_questions.id', ondelete='CASCADE'))
   
class Enrol_user(Base): 
   __tablename__ = 'tbl_enrol_user'
   id = Column(Integer, primary_key=True) 
   question_ids = Column(String(1000))
   complete_question = Column(String(45), default='na')
   user_id = Column(Integer,ForeignKey('tbl_users.id', ondelete='CASCADE'))
   lesson_id = Column(Integer,ForeignKey('tbl_lessons.id', ondelete='CASCADE')) 

class User_answer(Base):
   __tablename__ = 'tbl_user_answers'
   id = Column(Integer, primary_key=True)  
   ans_no = Column(String(45))
   user_id = Column(Integer,ForeignKey('tbl_users.id', ondelete='CASCADE'))
   question_id = Column(Integer,ForeignKey('tbl_questions.id', ondelete='CASCADE'))
   lesson_id = Column(Integer,ForeignKey('tbl_lessons.id', ondelete='CASCADE'))
   

class Sale_plan(Base):
   __tablename__ = 'tbl_sale_plan'
   id = Column(Integer, primary_key=True)  
   title = Column(String(45))
   price = Column(String(45))
   lessons = Column(String(200))
   invoice = relationship('Invoice') 

class Invoice(Base):
   __tablename__ = 'tbl_invoices'
   id = Column(Integer, primary_key=True)  
   invoice_no = Column(String(200))
   datetime = Column(String(100))
   transaction_reference_id = Column(String(200))
   status = Column(String(45))
   lessons = Column(String(200))
   verify = Column(String(100))
   user_id = Column(Integer,ForeignKey('tbl_users.id', ondelete='CASCADE'))
   sale_plan_id = Column(Integer,ForeignKey('tbl_sale_plan.id', ondelete='CASCADE'))



     



