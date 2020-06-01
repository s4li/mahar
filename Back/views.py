from flask import Flask, jsonify, request, redirect, render_template
from flask_cors import CORS
from functools import wraps
from suds.client import Client
from datetime import datetime, timedelta
from sqlalchemy.sql import func
import jwt, json, hashlib, hmac
from random import randint
from user_agents import parse
from flask_bcrypt import Bcrypt
from Back.conection_info import front_url, back_url
from Back.models import  (Session, User, Course, Lesson, Answer, 
                     Question, User_answer, Voice, Sale_plan, Invoice, Enrol_user)


app = Flask(__name__)

# enable CORS
CORS(app)
app.secret_key = 'In the name of Allah!'

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
                session.commit()
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

def check_user_access(user_id, lesson_id):
    session = Session()
    user_purchased_lessons = session.query(User.purchased_lessons).filter(User.id == user_id).first()
    purchased_lessons_list = user_purchased_lessons[0].split(',')
    user_access_lesson = True if f'{lesson_id}' in purchased_lessons_list else False
    session.commit()
    session.close()
    return user_access_lesson
       
def make_hashed_password(password):
    hashed_key= 'test1234567879'
    h = hashlib.blake2b(key= hashed_key.encode(), digest_size=16)
    h.update(password[:512].encode()) # limit password to 512 characters. 
    hash_password = h.hexdigest().encode('utf-8')
    return hash_password

def send_sms(mobile, sms_text):
    from suds.client import Client
    url="http://ws.smartsms.ir/sms.asmx?WSDL"
    client = Client(url, timeout=240)
    originator = '50002237167'#500059962
    message= '''
    <xmsrequest>
    <userid>53741</userid>
    <password>Salam159!</password>
    <action>smssend</action>
    <body>
    <type>oto</type>
    '''+\
    '<recipient mobile="{}" originator="{}" >{}</recipient>'.format(mobile,originator,sms_text) +\
    '''
    </body>
    </xmsrequest>
    '''
    response = client.service.XmsRequest(requestData= message)
    result= False
    if '<code id="0">ok</code>' in response:
        result= True
    return result

@app.route('/api/confirm-mobile')
def confirm_mobile(): 
    session = Session()
    mobile = request.args['mobile']
    user = session.query(User).filter(User.mobile == mobile).first()
    if user:
        code = randint(10000, 99999)
        text = f' {code} : کد تایید مهار'
        confirm_sms = send_sms(mobile, text)
        if confirm_sms:
            response = {'result':'success'}
            session.query(User).filter(User.id == user.id).update({ User.confirm_code: code})
            session.commit()
            status_code = 200
        else:
            response = {'result':'ارسال پیامک ناموفق بود!'} 
            status_code = 401  
    else:
        response = {'result':'کاربر گرامی، اطلاعاتی با این شماره موبایل ثبت نشده است!'} 
        status_code = 401 
    session.commit()      
    session.close()      
    return jsonify(response), status_code

@app.route('/api/reset-password', methods=('POST',))
def reset_password(): 
    session = Session()
    data = request.get_json()
    user = session.query(User).filter(User.mobile == data['mobile']).first()
    if user and user.confirm_code == data['confirm_code']:
        if data['password'] == data['re_password']:
            hash_password = make_hashed_password(data['password'])
            session.query(User).filter(User.id == user.id).update({ User.password : hash_password})
            session.commit()
            status_code = 200
            response = {'result': 'رمزعبور با موفقیت تغییر یافت.'}
        else:
            response = {'result': 'رمزهای ورودی با هم مطاقبت ندارد!'} 
            status_code = 401
    else:
        response = {'result': 'کد تایید مطابقت ندارد!'} 
        status_code = 401  
    session.commit()      
    session.close()           
    return jsonify(response), status_code

@app.route('/api/register', methods=('POST',))
def register():
    session = Session()
    data = request.get_json()
    user = session.query(User).filter(User.mobile == data['mobile']).first()
    if data and user == None :
        hash_password = make_hashed_password(data['password'])
        user = User(full_name = data['full_name'], mobile = data['mobile'], password = hash_password)
        session.add(user)
        session.commit()
        token = jwt.encode({
                            'sub': user.mobile,
                            'iat':datetime.utcnow()},
                            app.secret_key)
        #iat: the time the jwt was issued at
        #exp : is the moment the jwt should expire  
        response = {'result':f'{user.full_name}عزیز شما با موفقیت ثبت نام شدید.', 'full_name': user.full_name, 'token':token.decode('UTF-8'), 'id': user.id}
        status_code = 200
    else:
        response = {'result':'کاربر عزیز، با این شماره موبایل قبلا ثبت نام شده، در صورت فراموشی رمز "فراموشی کلمه عبور" را لمس نمایید. '}
        status_code = 401 
    session.commit()      
    session.close()                           
    return jsonify(response), status_code

@app.route('/api/login', methods=('POST',))
def login():
    session = Session() 
    data = request.get_json()
    user = session.query(User).filter(User.mobile == data['mobile']).first()
    if user:
        good_sig = make_hashed_password(data['password'])
        check_if_password_is_correct = hmac.compare_digest(good_sig, bytes(user.password , encoding= 'utf-8'))
        if  check_if_password_is_correct:
            token = jwt.encode({ 
                        'sub' : user.mobile,
                        'iat' : datetime.utcnow()
                            },
                            app.secret_key  
                          )
            status_code = 200                  
            response = {'result': f'{user.full_name}عزیز خوش آمدید.', 'token': token.decode('UTF-8'), 'full_name': user.full_name, 'id' : user.id} 
        else:
            status_code = 401
            response = {'result':'رمز عبور خود را درست وارد نکرده اید!'} 
    else:
        status_code = 401
        response = {'result':'این نام کاربری قبلا ثبت نام نشده است!'} 
    session.commit()    
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
    session.commit()    
    session.close()                  
    return jsonify(response), status_code    

@app.route('/api/courses')     
@token_required 
def courses(cuser):
    session = Session()
    user_id = int(request.args['user_id'])
    all_courses = []
    courses = session.query(Course).all()
    if courses:
        for course in courses:
            lesson = session.query(Lesson).filter(Lesson.course_id == course.id).first()
            has_content = True if lesson else False
            all_courses.append({"id": course.id, "title":course.title, "has_content": has_content})
    user = session.query(User).filter(User.id == user_id).first()
    user_purchased_lessons = user.purchased_lessons.split(',')
    complete_information = False
    if len(user_purchased_lessons) > 6 and user.grade == 'na':
        complete_information = True  
    response = {'all_courses' : all_courses, 'complete_information': complete_information}
    session.commit()
    session.close()     
    return jsonify(response)

@app.route('/api/lessons')     
@token_required
def lessons(cuser):
    session = Session()
    course_id = int(request.args['course_id'])
    user_id = int(request.args['user_id'])
    all_lessons = []
    lessons = session.query(Lesson).filter(Lesson.course_id == course_id).all()
    user_purchased_lessons = session.query(User.purchased_lessons).filter(User.id == user_id).first()
    purchased_lessons_list = user_purchased_lessons[0].split(',')
    for lesson in lessons:
        show_lesson = True if f'{lesson.id}' in purchased_lessons_list else False
        all_lessons.append({"id": lesson.id, "title":lesson.title, "show_lesson":show_lesson}) 
    session.commit()
    session.close()        
    return jsonify(all_lessons)    

@app.route('/api/get-status-question-user')     
@token_required
def status_question(cuser):
    lesson_id = int(request.args['lesson_id'])
    user_id = int(request.args['user_id'])
    has_access = check_user_access(user_id, lesson_id)
    if has_access:
        session = Session()
        has_new_question = session.query(Question).filter(Question.lesson_id == lesson_id).first()
        check_new_question = 'True' if has_new_question else 'False'
        enrol_user = session.query(Enrol_user.complete_question).filter(Enrol_user.lesson_id == lesson_id, Enrol_user.user_id == user_id).first()
        check_continue_previous_questions = 'False'
        if enrol_user and enrol_user[0] != 'True':
            check_continue_previous_questions = 'True'
        has_wrong_questions = session.query(User_answer.question_id).filter(User_answer.user_id == user_id, User_answer.ans_no == 1, User_answer.lesson_id == lesson_id).first()
        check_wrong_questions = 'True' if has_wrong_questions else 'False'
        result = {"check_new_question":check_new_question, "review_previous_questions":check_continue_previous_questions, "check_wrong_questions":check_wrong_questions}
        status_code = 200
        session.commit()
        session.close() 
    else:
        status_code = 401
        result = {"result" : "The user does not have access"}
    return jsonify(result), status_code

@app.route('/api/new-questions')     
@token_required
def new_questions(cuser): 
    lesson_id = int(request.args['lesson_id'])
    user_id = int(request.args['user_id'])
    has_access = check_user_access(user_id, lesson_id)
    if has_access:
        session = Session()
        index = int(request.args['index'])
        if index == -1 :
            all_previous_answer = session.query(User_answer).filter(User_answer.lesson_id == lesson_id, User_answer.user_id == user_id).all()
            if all_previous_answer:
                for answer in all_previous_answer:
                    session.delete(answer)
                    session.commit()
            has_user_enrol = session.query(Enrol_user).filter(Enrol_user.lesson_id == lesson_id, Enrol_user.user_id == user_id).first()          
            if has_user_enrol:
                session.query(Enrol_user).filter(Enrol_user.lesson_id == lesson_id, Enrol_user.user_id == user_id).update({ Enrol_user.complete_question: 'na' , Enrol_user.question_ids : 'na'})
                session.commit()
            else:
                enrol_user = Enrol_user(lesson_id = lesson_id, user_id=user_id, complete_question =  'na', question_ids = 'na')
                session.add(enrol_user)  
                session.commit()   
        user_enrol = session.query(Enrol_user).filter(Enrol_user.lesson_id == lesson_id, Enrol_user.user_id == user_id).first()             
        question_len = session.query(Question).filter(Question.lesson_id == lesson_id).count()
        if user_enrol.question_ids != 'na' :
            user_question_ids = user_enrol.question_ids.split(',')
            user_question_ids_len = len(user_question_ids)
        else:
            user_question_ids = [0]
            user_question_ids_len = 0
        next_new_question = 'na' 
        while user_question_ids_len + 1 < question_len:
            random_question = session.query(Question).order_by(func.rand()).filter(Question.lesson_id == lesson_id).first()
            if str(random_question.id) not in user_question_ids:
                next_new_question = random_question
                break    
        if next_new_question == 'na':
            first_question_id = session.query(Question.id).filter(Question.lesson_id == lesson_id).first()
            last_question_id = session.query(Question.id).order_by(Question.id.desc()).filter(Question.lesson_id == lesson_id).first()
            for id in range(int(first_question_id[0]), int(last_question_id[0])):
                if id not in user_question_ids:
                    next_new_question = session.query(Question).filter(Question.id == id).first()
                    break
        next_new_voice = session.query(Voice).filter(Voice.id == next_new_question.voice_id).first()
        next_new_answer = session.query(Answer).filter(Answer.question_id == next_new_question.id).first()
        lesson = session.query(Lesson).filter(Lesson.id == lesson_id).first()      
        result = {"question":next_new_question.text, "voice":f'{next_new_voice.path}', "next_index":next_new_question.id, "question_id": next_new_question.id, "answer": next_new_answer.ans_text, "lesson_title":lesson.title}
        status_code = 200
        session.commit()
        session.close() 
    else:
        status_code = 401
        result = {"result" : "The user does not have access"}    
    return jsonify(result), status_code    

@app.route('/api/get-previous-questions')     
@token_required
def continue_previous_questions(cuser): 
    user_id = int(request.args['user_id'])
    lesson_id = int(request.args['lesson_id'])
    has_access = check_user_access(user_id, lesson_id)
    if has_access:
        session = Session()
        index = int(request.args['index'])
        question_len = session.query(Question).filter(Question.lesson_id == lesson_id).count()
        user_enrol = session.query(Enrol_user).filter(Enrol_user.user_id== user_id, Enrol_user.lesson_id == lesson_id).first()
        if user_enrol.question_ids :
            user_question_ids = user_enrol.question_ids.split(',')
            user_question_ids_len = len(user_question_ids)
        else:
            user_question_ids = 'na'
            user_question_ids_len = 0
        next_continue_previous_question = 'na'     
        while user_question_ids_len + 1 < question_len:
            random_question = session.query(Question).order_by(func.rand()).filter(Question.lesson_id == lesson_id).first()
            if str(random_question.id) not in user_question_ids:
                next_continue_previous_question = random_question
                break   
        if next_continue_previous_question == 'na':
            first_question_id = session.query(Question.id).filter(Question.lesson_id == lesson_id).first()
            last_question_id = session.query(Question.id).order_by(Question.id.desc()).filter(Question.lesson_id == lesson_id).first()
            for id in range(int(first_question_id[0]), int(last_question_id[0])):
                if id not in user_question_ids:
                    next_continue_previous_question = session.query(Question).filter(Question.id == id).first()
                    break    
        next_continue_previous_voice = session.query(Voice).filter(Voice.id == next_continue_previous_question.voice_id).first()
        next_continue_previous_answer = session.query(Answer).filter(Answer.question_id == next_continue_previous_question.id).first()
        lesson = session.query(Lesson).filter(Lesson.id == lesson_id).first()
        result = {"question":next_continue_previous_question.text, "voice": f'{next_continue_previous_voice.path}', "next_index": next_continue_previous_question.id , "question_id": next_continue_previous_question.id, "answer": next_continue_previous_answer.ans_text,  "lesson_title":lesson.title}
        status_code = 200
        session.commit()
        session.close() 
    else:
        status_code = 401
        result = {"result" : "The user does not have access"}     
    return jsonify(result), status_code

@app.route('/api/get-wrong-questions')     
@token_required
def wronge_questions(cuser): 
    user_id = int(request.args['user_id'])
    lesson_id = int(request.args['lesson_id'])
    has_access = check_user_access(user_id, lesson_id)
    if has_access:
        session = Session()
        index = int(request.args['index'])
        first_wrong_answer = session.query(User_answer).order_by(User_answer.question_id.asc()).filter(User_answer.user_id == user_id, User_answer.question_id> f'{index}', User_answer.ans_no == '1', User_answer.lesson_id == lesson_id).first()
        next_wrong_question = session.query(Question).filter(Question.id == first_wrong_answer.question_id).first()
        next_wrong_voice = session.query(Voice).filter(Voice.id == next_wrong_question.voice_id).first()
        next_wrong_answer = session.query(Answer).filter(Answer.question_id == next_wrong_question.id).first()
        lesson = session.query(Lesson).filter(Lesson.id == lesson_id).first()
        result = {"question":next_wrong_question.text, "voice": f'{next_wrong_voice.path}', "next_index": next_wrong_answer.question_id , "question_id": next_wrong_question.id, "answer": next_wrong_answer.ans_text,  "lesson_title":lesson.title}
        status_code = 200
        session.commit()
        session.close() 
    else:
        status_code = 401
        result = {"result" : "The user does not have access"}    
    return jsonify(result), status_code

@app.route('/api/set-user-answer', methods=('POST',))    
@token_required
def user_answer(cuser): 
    data = request.get_json()
    has_access = check_user_access(data['user_id'], data['lesson_id'])
    if has_access:
        session = Session()
        user_previous_answer  = session.query(User_answer.id).filter(User_answer.user_id == data['user_id'], User_answer.question_id == data['question_id']).first()
        if not user_previous_answer :
            user_answer = User_answer(ans_no=data['ans_no'], user_id=data['user_id'], question_id=data['question_id'], lesson_id=data['lesson_id'])
            session.add(user_answer)
            session.commit()
        else:
            user_answer_update = session.query(User_answer).filter(User_answer.id == user_previous_answer[0]).update({User_answer.ans_no : data['ans_no']}) 
            session.commit()
        user_question_ids = session.query(Enrol_user.question_ids).filter(Enrol_user.lesson_id == data['lesson_id'], Enrol_user.user_id == data['user_id']).first()  
        if user_question_ids[0] != 'na':
            complete_user_question_ids = user_question_ids[0] + ',' + str(data['question_id'])
            user_question_ids_len = len(user_question_ids[0].split(','))
        else:
            complete_user_question_ids = str(data['question_id'])
            user_question_ids_len = 1 
        questions_len = session.query(Question).filter(Question.lesson_id == data['lesson_id']).count() 
        if data['question_type'] == 1:
            next_content = False
            complete_question = 'True'
            if user_question_ids_len + 1 < questions_len:
                next_content = True
                complete_question = 'False' 
            session.query(Enrol_user).filter(Enrol_user.lesson_id == data['lesson_id'], Enrol_user.user_id == data['user_id']).update({ Enrol_user.complete_question: complete_question, Enrol_user.question_ids : complete_user_question_ids})
            session.commit()
        elif data['question_type'] == 2:
            next_content = False
            complete_question = 'True'
            if user_question_ids_len + 1 < questions_len:
                next_content = True 
                complete_question = 'False' 
            session.query(Enrol_user).filter(Enrol_user.lesson_id == data['lesson_id'], Enrol_user.user_id == data['user_id']).update({ Enrol_user.complete_question: complete_question , Enrol_user.question_ids : complete_user_question_ids})
            session.commit()
        else:
            next_content = session.query(User_answer).order_by(User_answer.question_id.asc()).filter(User_answer.user_id == data['user_id'], User_answer.question_id> data['question_id'], User_answer.ans_no == '1', User_answer.lesson_id == data['lesson_id']).first()
        if next_content:
            result = {"has_next_new_question":"True"}
        else:
            wrong_answer_no = session.query(func.count(User_answer.id)).order_by(User_answer.lesson_id).filter(User_answer.user_id == data['user_id'] ,User_answer.ans_no == '1', User_answer.lesson_id == data['lesson_id']).scalar() 
            true_answer_no = session.query(func.count(User_answer.id)).order_by(User_answer.lesson_id).filter(User_answer.user_id == data['user_id'],  User_answer.ans_no == '0', User_answer.lesson_id == data['lesson_id']).scalar() 
            result = {"has_next_new_question":"False", "wrong_answer_no":wrong_answer_no, "true_answer_no":true_answer_no}    
        status_code = 200
        session.commit()
        session.close()
    else:
        status_code = 401
        result = {"result" : "The user does not have access"}    
    return  jsonify(result), status_code

@app.route('/api/zarinpal/<type>/<user_id>/<sale_plan_id>/<course_id>')
@token_required    
def zarinpal(cuser, type, user_id, sale_plan_id, course_id): 
    session = Session()
    ZARINPAL_WEBSERVICE  = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'
    MMERCHANT_ID = '46c993a0-9bed-11ea-8c18-000c295eb8fc'
    invoice_date= datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    client = Client(ZARINPAL_WEBSERVICE)
    sale_plan = session.query(Sale_plan).filter(Sale_plan.id == sale_plan_id).first()
    user = session.query(User).filter(User.id == user_id).first()
    if not (sale_plan or user):
        result = {"result":"user or sale plane id not found"}
        status_code = 401
    else:
        callback_url = f'{back_url}/api/zarinpal-callback' 
        result_zarinpal = client.service.PaymentRequest(MMERCHANT_ID,
                                           sale_plan.price,
                                           sale_plan.title,
                                           user.mobile,
                                           'tajbakhsh.ut.ac@gmail.com',
                                           callback_url)
        if result_zarinpal.Status == 100:
            if sale_plan_id == '2' : 
                lesson_ids = session.query(Lesson.id).filter(Lesson.course_id == course_id).all()
                str_lesson = ''
                for lesson_id in lesson_ids:
                    if str(lesson_id[0]) not in ['1','9','16','20','32','42']:
                        str_lesson = str_lesson +str(lesson_id[0]) + ","
                lessons = str_lesson[:-1]
            else:
                lessons = sale_plan.lessons        
            invoice = Invoice( invoice_no = result_zarinpal.Authority,  datetime = invoice_date , sale_plan_id = sale_plan_id, user_id = user_id, lessons = lessons, verify= -1)
            session.add(invoice)
            session.commit()
            session.close()
            zarinpal_url = f'https://www.zarinpal.com/pg/StartPay/{result_zarinpal.Authority}'
            result = {"result":"success", "zarinpal_url":zarinpal_url}
            status_code = 200
        else:
            result = {"result":f'{user.full_name} عزیز، با عرض پوزش در هنگام اتصال به درگاه بانک خطایی رخ داده است.'}
            status_code = 401
    session.commit()        
    session.close()         
    return jsonify(result)  

@app.route('/api/zarinpal-callback')    
def zarinpal_callback():
    session = Session()
    ZARINPAL_WEBSERVICE  = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'    
    MMERCHANT_ID = '46c993a0-9bed-11ea-8c18-000c295eb8fc'
    print(MMERCHANT_ID)
    client = Client(ZARINPAL_WEBSERVICE)
    Status = request.args['Status'] 
    print(f'{Status}')
    Authority = request.args['Authority']
    if Status == 'OK':
        check_invoice = session.query(Invoice).filter(Invoice.invoice_no == Authority).first()
        if check_invoice:
            sale_plan = session.query(Sale_plan.price).filter(check_invoice.sale_plan_id == Sale_plan.id).first()
            result_zarinpal = client.service.PaymentVerification(MMERCHANT_ID,
                                                                Authority,
                                                                sale_plan[0])                                                                                                                                   
            if  result_zarinpal.Status == 100: 
                zarinpal_result_status = result_zarinpal.Status
                user = session.query(User).filter(User.id == check_invoice.user_id).first()
                result = {'result': f'{user.full_name}عزیز پرداخت شما موفق بوده است.'} 
                status_code = 200 
                old_purchased_lessons = session.query(User.purchased_lessons).filter(User.id == check_invoice.user_id).first()
                new_purchased_lessons = check_invoice.lessons 
                new_purchased_lessons_split = new_purchased_lessons.split(',')
                old_purchased_lessons_split = old_purchased_lessons[0].split(',')
                purchased_lessons = old_purchased_lessons[0]
                for lesson in new_purchased_lessons_split:
                    if lesson not in old_purchased_lessons_split:
                        purchased_lessons = purchased_lessons  + ',' + lesson
                update_user = session.query(User).filter(User.id == check_invoice.user_id).update({User.purchased_lessons : purchased_lessons})  
                session.commit()
                 
                    #return 'Transaction success. RefID: ' + str(result.RefID)   
            elif result_zarinpal.Status == 101:
                zarinpal_result_status = result_zarinpal.Status
                user = session.query(User).filter(User.id == check_invoice.user_id).first()
                result = {'result': f'{user.full_name}عزیز پرداخت شما موفق بوده است.'} 
                status_code = 200
                if check_invoice.sale_plan_id == 1:
                    purchased_lessons = check_invoice.lessons
                else : 
                    purchased_lessons_user = session.query(User.purchased_lessons).filter(User.id == check_invoice.user_id).first()
                    purchased_lessons = check_invoice.lessons + purchased_lessons_user[0] 
                update_user = session.query(User).filter(User.id == check_invoice.user_id).update({User.purchased_lessons : purchased_lessons})  
                session.commit()
                  
                #return 'Transaction submitted : ' + str(result.Status)
            else:
                zarinpal_result_status = result_zarinpal.Status
                result = {'result': 'عملیات پرداخت ناموفق بود.'} 
                status_code = 401 
                #return 'Transaction failed. Status: ' + str(result.Status)
            invoice = session.query(Invoice).filter(Invoice.invoice_no == Authority).update({Invoice.status : zarinpal_result_status, Invoice.transaction_reference_id: result_zarinpal.RefID})       
    else:  
        invoice = session.query(Invoice).filter(Invoice.invoice_no == Authority).update({Invoice.status : Status})   
        session.commit()
        result = {'result': 'عملیات پرداخت توسط کاربر یا سیستم متوقف شد.'} 
        status_code = 401 
        #return 'Transaction failed or canceled by user'
        session.commit()
        session.close()
        return redirect("/Grades")  
        

@app.route('/api/mobile/zarinpal-callback', methods=['GET',])
def api_pasargad_callback():
    session = Session()
    verify = request.form.get('verify')
    bills_status = session.query(Invoice.status).filter(Invoice.verify == verify).first()
    if bills_status:
        transactionID = bills_status[0]
    else:
        transactionID = None
    dict_data={"transaction" : transactionID}
    session.commit()
    session.close()
    return dict_data

@app.route('/api/information-completion-status' , methods=('POST',))    
@token_required
def information_completion_status(cuser):
    session = Session()
    data = request.get_json()
    user = session.query(User).filter(User.id == data['user_id']).update({User.grade : data['grade'], User.city : data['city']})   
    session.commit()
    session.close()
    return jsonify("True")

@app.route('/api/get-user-agent')    
def get_user_agent():
    ua_string = request.headers.get('User-Agent')
    user_agent = parse(ua_string)
    is_mobile = user_agent.is_mobile # returns True or false
    is_tablet = user_agent.is_tablet 
    is_touch_capable = user_agent.is_touch_capable 
    is_pc = user_agent.is_pc 
    is_bot = user_agent.is_bot 
    if is_mobile:
        user_agent_type = 'mobile'  
    elif is_tablet:
        user_agent_type = 'tablet'
    elif is_touch_capable:
        user_agent_type = 'touch_capable'
    elif is_pc:
        user_agent_type = 'pc'  
    else:
        user_agent_type = 'bot'         
    return jsonify(user_agent_type) 

if __name__ == '__main__':
    app.run(debug=True) 