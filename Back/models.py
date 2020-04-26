from sqlalchemy import Column, Table, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base #class stores a catlog of classes and mapped tables in the Declarative system
from sqlalchemy.orm import sessionmaker, relationship
import pymysql
from conection_info import password, user


engine = create_engine(f'mysql+pymysql://{user}:{password}@localhost/mahar?charset=utf8') # Create the database in memory
Base = declarative_base() #function is used to create base class
Session = sessionmaker(bind = engine) # A session object is the handle to database
session = Session()

class User(Base):
   __tablename__ = 'tbl_users'
   id = Column(Integer, primary_key=True)
   full_name = Column(String)
   mobile = Column(String)
   password = Column(String)

class Course(Base):
   __tablename__ = 'tbl_courses'
   id = Column(Integer, primary_key=True)  
   title = Column(String)

class Lesson(Base):
   __tablename__ = 'tbl_lessons'
   id = Column(Integer, primary_key=True)  
   title = Column(String)
   course_id = Column(Integer,ForeignKey('tbl_courses.id', ondelete='CASCADE'))
   course = relationship('Course', backref='lessons')

class Voice(Base):
   __tablename__ = 'tbl_voices'
   id = Column(Integer, primary_key=True)  
   title = Column(String)
   path = Column(String)
   lesson_id = Column(Integer,ForeignKey('tbl_lessons.id', ondelete='CASCADE'))
   lesson = relationship('Lesson', backref='voices')   

class Question(Base):
   __tablename__ = 'tbl_questions'
   id = Column(Integer, primary_key=True)  
   text = Column(String)
   path = Column(String)
   lesson_id = Column(Integer,ForeignKey('tbl_lessons.id', ondelete='CASCADE'))
   voice_id = Column(Integer,ForeignKey('tbl_voices.id', ondelete='CASCADE'))
   lesson = relationship('Lesson', backref='questions')  
   voice = relationship('Voice', backref='questions') 

class Answer(Base):
   __tablename__ = 'tbl_answers'
   id = Column(Integer, primary_key=True)  
   ans_text = Column(String)
   check_ans = Column(String)
   question_id = Column(Integer,ForeignKey('tbl_questions.id', ondelete='CASCADE'))
   question = relationship('Question', backref='answers')

class User_answer(Base):
   __tablename__ = 'tbl_users_answers'
   id = Column(Integer, primary_key=True)  
   ans_no = Column(String)
   user_id = Column(Integer,ForeignKey('tbl_users.id', ondelete='CASCADE'))
   answer_id = Column(Integer,ForeignKey('tbl_answers.id', ondelete='CASCADE'))
   user = relationship('User', backref='answers')  
   answer = relationship('Answer', backref='answers') 

class Sale_plan(Base):
   __tablename__ = 'tbl_sale_plan'
   id = Column(Integer, primary_key=True)  
   title = Column(String)
   price = Column(String)

class Invoice(Base):
   __tablename__ = 'tbl_invoices'
   id = Column(Integer, primary_key=True)  
   title = Column(String)
   invoice_no = Column(String)
   datetime = Column(String)
   transaction_reference_id = Column(String)
   status = Column(String)
   user_id = Column(Integer,ForeignKey('tbl_users.id', ondelete='CASCADE'))
   sale_plan_id = Column(Integer,ForeignKey('tbl_sale_plan.id', ondelete='CASCADE'))
   user = relationship('User', backref='invoices')  
   sale_plan = relationship('Sale_plan', backref='invoices')    



