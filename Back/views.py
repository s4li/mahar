from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from functools import wraps
from suds.client import Client
from .models import  Session, User, Course, Lesson, Answer, Question, User_answer, Voice, Sale_plan, Invoice, Enrol_user
from datetime import datetime, timedelta
from sqlalchemy.sql import func
import jwt, json

app = Flask(__name__)
app.secret_key = 'mahar'

# enable CORS
CORS(app)

root_url = 'http://localhost:5555'

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        session = Session()
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, app.secret_key)
            user = None
            if data and data['sub']:
                user = session.query(User).filter_by(mobile=data['sub']).first()
                session.close()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify
  
    
@app.route('/api/register', methods=('POST',))
def register():
    session = Session()
    data = request.get_json()
    user = session.query(User).filter(User.mobile == data['mobile']).first()
    if user == None:
        user = User(full_name = data['full_name'], mobile = data['mobile'], password = data['password'])
        session.add(user)
        session.commit()
        status_code = 200
        token = jwt.encode({
                            'sub': user.mobile,
                            'iat':datetime.utcnow(),  
                            'exp': datetime.utcnow() + timedelta(hours=24)},
                            app.secret_key)
        #iat: the time the jwt was issued at
        #exp : is the moment the jwt should expire  
        response = {'result':'success', 'full_name': user.full_name, 'token':token.decode('UTF-8'), 'id': user.id}
    else:
        response = {'result':'user_exists'}
        status_code = 401   
    session.close()                           
    return jsonify(response), status_code

@app.route('/api/login', methods=('POST',))
def login():
    session = Session() 
    data = request.get_json()
    user = session.query(User).filter(User.mobile == data['mobile'], User.password == data['password']).first()
    if user:
        token = jwt.encode({ 
                        'sub' : user.mobile,
                        'iat' : datetime.utcnow(),
                        'exp' : datetime.utcnow() + timedelta(hours=24)
                            },
                            app.secret_key  
                          )
        status_code = 200                  
        response = {'result': 'success', 'token': token.decode('UTF-8'), 'full_name': user.full_name, 'id' : user.id} 
    else:
        status_code = 401
        response = {'result':'nouser'} 
    session.close()                
    return jsonify(response), status_code

@app.route('/api/get-user-information')
@token_required
def user_information(cuser):
    session = Session()
    user_id = int(request.args['id']) 
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        response = {'result': 'success', 'full_name': user.full_name, 'mobile': user.mobile}
        status_code = 200
    else:
        status_code = 401
        response = {'result':'nouser'}
    session.close()                  
    return jsonify(response), status_code    

@app.route('/api/courses')     
@token_required
def courses(cuser):
    session = Session()
    all_courses = []
    courses = session.query(Course).all()
    for course in courses:
        lesson = session.query(Lesson).filter(Lesson.course_id == course.id).first()
        has_content = True if lesson else False
        all_courses.append({"id": course.id, "title":course.title, "has_content": has_content})
    session.close()     
    return jsonify(all_courses)

@app.route('/api/lessons')     
@token_required
def lessons(cuser):
    session = Session()
    course_id = int(request.args['course_id'])
    user_id = int(request.args['user_id'])
    all_lessons = []
    lessons = session.query(Lesson).filter(Lesson.course_id == course_id).all()
    user_purchased_lessons = session.query(User.purchased_lessons).filter(User.id == user_id).first()
    purchased_lessons = user_purchased_lessons[0].split(',')
    for lesson in lessons:
        show_lesson = True if f'{lesson.id}' in purchased_lessons else False
        all_lessons.append({"id": lesson.id, "title":lesson.title, "show_lesson":show_lesson}) 
    session.close()        
    return jsonify(all_lessons)    

@app.route('/api/get-status-question-user')     
@token_required
def status_question(cuser):
    session = Session()
    lesson_id = int(request.args['lesson_id'])
    user_id = int(request.args['user_id'])
    has_new_question = session.query(Question).filter(Question.lesson_id == lesson_id).first()
    check_new_question = 'True' if has_new_question else 'False'
    enrol_user = session.query(Enrol_user.question_id).filter(Enrol_user.lesson_id == lesson_id, Enrol_user.user_id == user_id).first()
    check_previous_questions = 'False'
    if enrol_user and enrol_user[0] != -1:
        has_next_previous_question = session.query(Question).order_by(Question.id.asc()).filter( Question.id > enrol_user[0], Question.lesson_id == lesson_id ).first()
        check_previous_questions = 'True' if has_next_previous_question else 'False'
    has_wrong_questions = session.query(User_answer.question_id).filter(User_answer.user_id == user_id, User_answer.ans_no == 1, User_answer.lesson_id == lesson_id).first()
    check_wrong_questions = 'True' if has_wrong_questions else 'False'
    result = {"check_new_question":check_new_question, "review_previous_questions":check_previous_questions, "check_wrong_questions":check_wrong_questions}
    session.close() 
    return jsonify(result)

@app.route('/api/new-questions')     
@token_required
def all_questions(cuser): 
    session = Session()
    lesson_id = int(request.args['lesson_id'])
    index = int(request.args['index'])
    user_id = int(request.args['user_id'])
    next_new_question = session.query(Question).order_by(Question.id.asc()).filter(Question.id > f'{index}', Question.lesson_id == lesson_id).first()
    next_new_voice = session.query(Voice).filter(Voice.id == next_new_question.voice_id).first()
    next_new_answer = session.query(Answer).filter(Answer.question_id == next_new_question.id).first()
    if index == -1 :
        # delete all answer user and change status in enrol_user table
        all_previous_answer = session.query(User_answer).filter(User_answer.lesson_id == lesson_id, User_answer.user_id == user_id).all()
        if all_previous_answer:
            for answer in all_previous_answer:
                session.delete(answer)
                session.commit()
        has_enroll_user = session.query(Enrol_user).filter(Enrol_user.lesson_id == lesson_id, Enrol_user.user_id == user_id).first()   
        first_lesson_id = session.query(Question.id).filter(Question.lesson_id == lesson_id).first()
        if has_enroll_user:
            session.query(Enrol_user).filter(Enrol_user.lesson_id == lesson_id, Enrol_user.user_id == user_id).update({ Enrol_user.question_id: -1 })
            session.commit()
        else:
            enrol_user = Enrol_user(lesson_id = lesson_id, user_id=user_id, question_id =  -1)
            session.add(enrol_user)  
            session.commit()
    result = {"question":next_new_question.text, "voice":next_new_voice.path, "next_index":next_new_question.id, "question_id": next_new_question.id, "answer": next_new_answer.ans_text}
    session.close() 
    return jsonify(result)    

@app.route('/api/get-previous-questions')     
@token_required
def previous_questions(cuser): 
    session = Session()
    user_id = int(request.args['user_id'])
    lesson_id = int(request.args['lesson_id'])
    index = int(request.args['index'])
    enrol_user = session.query(Enrol_user.question_id).filter(Enrol_user.lesson_id == lesson_id, Enrol_user.user_id == user_id).first()
    previous_question = session.query(Question).order_by(Question.id.asc()).filter( Question.id> enrol_user[0], Question.lesson_id == lesson_id ).first()
    previous_voice = session.query(Voice).filter(Voice.id == previous_question.voice_id).first()
    previous_answer = session.query(Answer).filter(Answer.question_id == previous_question.id).first()
    result = {"question":previous_question.text, "voice": previous_voice.path, "next_index": previous_question.id , "question_id": previous_question.id, "answer": previous_answer.ans_text}
    session.close() 
    return jsonify(result)

@app.route('/api/get-wrong-questions')     
@token_required
def wronge_questions(cuser): 
    session = Session()
    user_id = int(request.args['user_id'])
    lesson_id = int(request.args['lesson_id'])
    index = int(request.args['index'])
    first_wrong_answer = session.query(User_answer).order_by(User_answer.question_id.asc()).filter(User_answer.user_id == user_id, User_answer.question_id> f'{index}', User_answer.ans_no == '1', User_answer.lesson_id == lesson_id).first()
    wrong_question = session.query(Question).filter(Question.id == first_wrong_answer.question_id).first()
    wrong_voice = session.query(Voice).filter(Voice.id == wrong_question.voice_id).first()
    wrong_answer = session.query(Answer).filter(Answer.question_id == wrong_question.id).first()
    result = {"question":wrong_question.text, "voice": wrong_voice.path, "next_index": wrong_answer.question_id , "question_id": wrong_question.id, "answer": wrong_answer.ans_text}
    session.close() 
    return jsonify(result)


@app.route('/api/set-user-answer', methods=('POST',))    
@token_required
def user_answer(cuser): 
    session = Session()
    data = request.get_json()
    user_previous_answer  = session.query(User_answer.id).filter(User_answer.user_id == data['user_id'], User_answer.question_id == data['question_id']).first()
    if not user_previous_answer :
        user_answer = User_answer(ans_no=data['ans_no'], user_id=data['user_id'], question_id=data['question_id'], lesson_id=data['lesson_id'])
        session.add(user_answer)
        session.commit()
    else:
        user_answer_update = session.query(User_answer).filter(User_answer.id == user_previous_answer[0]).update({User_answer.ans_no : data['ans_no']}) 
        session.commit()
    if data['question_type'] == 1:
        next_content = session.query(Question).order_by(Question.id.asc()).filter(Question.id > data['question_id'], Question.lesson_id == data['lesson_id']).first()
        session.query(Enrol_user).filter(Enrol_user.lesson_id == data['lesson_id'], Enrol_user.user_id == data['user_id']).update({ Enrol_user.question_id: data['question_id']})
        session.commit()
    elif data['question_type'] == 2:
        # update status in enrol
        next_content = session.query(Question).order_by(Question.id.asc()).filter( Question.id> data['question_id'] , Question.lesson_id == data['lesson_id']).first()
        session.query(Enrol_user).filter(Enrol_user.lesson_id == data['lesson_id'], Enrol_user.user_id == data['user_id']).update({ Enrol_user.question_id: data['question_id']})
        session.commit()
    else:
        next_content = session.query(User_answer).order_by(User_answer.question_id.asc()).filter(User_answer.user_id == data['user_id'], User_answer.question_id> data['question_id'], User_answer.ans_no == '1', User_answer.lesson_id == data['lesson_id']).first()
    if next_content:
        result = {"has_next_new_question":"True"}
    else:
        result = {"has_next_new_question":"False"}    
    session.close()
    return  jsonify(result)

@app.route('/api/zarinpall')    
@token_required
def zarinpal(cuser): 
    session = Session()
    user_id = int(request.args['user_id'])
    course_id = int(request.args['course_id'])
    sale_plan_id = int(request.args['sale_plan_id'])
    sale_plan = session.query(Sale_plan).filter(Sale_plan.id == sale_plan_id).first()
    user = session.query(User).filter(User.id == user_id).first()
    if not (sale_plan or user):
        result = {"result":"user or sale plane id not found"}
        status_code = 401
    else:
        ZARINPAL_WEBSERVICE  = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'
        MMERCHANT_ID = 'febd7482-570d-11e6-b65a-000c295eb8fc'
        callback_url = f'{root_url}/api/zarinpal-callback' 
        invoice_date= datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        client = Client(ZARINPAL_WEBSERVICE)
        result = client.service.PaymentRequest(MMERCHANT_ID,
                                           sale_plan.price,
                                           sale_plan.title,
                                           user.mobile,
                                           'parastoo.rambarzini@gmail.com',
                                           callback_url)
        if result.Status == 100:
            if sale_plan_id == 2 : 
                lesson_ids = session.query(Lesson.id).filter(Lesson.course_id == course_id).all()
                str_lesson = ''
                for lesson_id in lesson_ids:
                    if str(lesson_id[0]) not in ['1','9','16']:
                        str_lesson = str_lesson +str(lesson_id[0]) + ","
                lessons = str_lesson
            else:
                lessons = sale_plan.lessons        
            invoice = Invoice( invoice_no = result.Authority,  datetime = invoice_date , sale_plan_id = sale_plan_id, user_id = user_id, lessons = lessons)
            session.add(invoice)
            session.commit()
            session.close()
            zarinpal_url = f'https://www.zarinpal.com/pg/StartPay/{result.Authority}'
            result = {"result":"success", "zarinpal_url":zarinpal_url}
            status_code = 200
        else:
            result = {"result":"faild"}
            status_code = 401
    session.close()         
    return jsonify(result), status_code   

@app.route('/api/zarinpal-callback')    
def zarinpal_callback():
    session = Session()
    ZARINPAL_WEBSERVICE  = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'    
    MMERCHANT_ID = 'febd7482-570d-11e6-b65a-000c295eb8fc'
    client = Client(ZARINPAL_WEBSERVICE)
    Status = request.args['Status'] 
    Authority = request.args['Authority']
    if Status == 'OK':
        check_invoice = session.query(Invoice).filter(Invoice.invoice_no == Authority).first()
        if check_invoice:
            sale_plan = session.query(Sale_plan.price).filter(check_invoice.sale_plan_id == Sale_plan.id).first()
            result = client.service.PaymentVerification(MMERCHANT_ID,
                                                        Authority,
                                                        sale_plan[0])                                                                                                                                   
            if result.Status == 100:  
                result = {'result': 'success'} 
                status_code = 200 
                if check_invoice.sale_plan_id == 1:
                    purchased_lessons = check_invoice.lessons
                else : 
                    purchased_lessons_user = session.query(User.purchased_lessons).filter(User.id == check_invoice.user_id).first()
                    purchased_lessons = check_invoice.lessons + purchased_lessons_user[0] 
                update_user = session.query(User).filter(User.id == check_invoice.user_id).update({User.purchased_lessons : purchased_lessons})  
                session.commit()
                #return 'Transaction success. RefID: ' + str(result.RefID)   
            elif result.Status == 101:
                result = {'result': 'success'} 
                status_code = 200 
                #return 'Transaction submitted : ' + str(result.Status)
            else:
                result = {'result': 'feild'} 
                status_code = 401 
                #return 'Transaction failed. Status: ' + str(result.Status)
            invoice = session.query(Invoice).filter(Invoice.invoice_no == Authority).update({Invoice.status : result.Status, Invoice.transaction_reference_id: result.RefID})       
            session.commit()
    else:
        invoice = session.query(Invoice).filter(Invoice.invoice_no == Authority).update({Invoice.status : Status})   
        session.commit()
        result = {'result': 'feild'} 
        status_code = 401 
        #return 'Transaction failed or canceled by user'
    session.close() 
    return jsonify(result), status_code    


if __name__ == '__main__':
    app.run(debug=True) 