from flask import Flask, jsonify, request, redirect, render_template, flash, url_for, session as session_f
from suds.client import Client
from datetime import datetime, timedelta
from sqlalchemy.sql import func
import jwt, json, hashlib, hmac
from random import randint
from user_agents import parse
from flask_bcrypt import Bcrypt
from conection_info import front_url, back_url
from models import  (Session, User, Course, Lesson, Answer, 
                     Question, User_answer, Voice, Sale_plan, Invoice, Enrol_user)


app = Flask(__name__)


def check_user_access(user_id, lesson_id):
    s = Session()
    user_purchased_lessons = s.query(User.purchased_lessons).filter(User.id == user_id).first()
    purchased_lessons_list = user_purchased_lessons[0].split(',')
    user_access_lesson = True if f'{lesson_id}' in purchased_lessons_list else False
    s.commit()
    s.close()
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

@app.route('/')
def index():
    return  render_template('first-login.html') 

@app.route('/guids')
def guids():
    return  render_template('guids.html')

@app.route('/install-guids')
def install_guids():
    return  render_template('install-guids.html')

@app.route('/confirm-mobile')
def confirm_mobile(): 
    s = Session()
    mobile = request.args['mobile']
    user = s.query(User).filter(User.mobile == mobile).first()
    if user:
        code = randint(10000, 99999)
        text = f' {code} : کد تایید مهار'
        confirm_sms = send_sms(mobile, text)
        if confirm_sms:
            response = {'result':'success'}
            s.query(User).filter(User.id == user.id).update({ User.confirm_code: code})
            s.commit()
            return redirect("reset_password")
        else:
            flash('ارسال پیامک ناموفق بود!','danger') 
            return redirect("confirm_mobile")
    else:
        flash('کاربر گرامی، اطلاعاتی با این شماره موبایل ثبت نشده است!','danger')
        return redirect("register")
    s.commit()      
    s.close()      
    return  render_template('password-recovey.html')

@app.route('/reset-password', methods=('POST',))
def reset_password(): 
    s = Session()
    data = request.get_json()
    user = s.query(User).filter(User.mobile == data['mobile']).first()
    if user and user.confirm_code == data['confirm_code']:
        if data['password'] == data['re_password']:
            hash_password = make_hashed_password(data['password'])
            s.query(User).filter(User.id == user.id).update({ User.password : hash_password})
            s.commit()
            status_code = 200
            response = {'result': 'رمزعبور با موفقیت تغییر یافت.'}
        else:
            response = {'result': 'رمزهای ورودی با هم مطاقبت ندارد!'} 
            status_code = 401
    else:
        response = {'result': 'کد تایید مطابقت ندارد!'} 
        status_code = 401  
    s.commit()      
    s.close()           
    return  render_template('signup.html')

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        s = Session()
        mobile = request.form.get('mobile')
        user = s.query(User).filter(User.mobile == mobile).first()
        if user == None :
            full_name = request.form.get('full_name')
            password = request.form.get('password')
            hash_password = make_hashed_password(password)
            user = User(full_name = full_name, mobile =mobile, password = hash_password)
            s.add(user)
            s.commit()
            session_f['user_id'] = user.id
            flash(f'{user.full_name}عزیز شما با موفقیت ثبت نام شدید.','success')
            return redirect(url_for("grades"))
        else:
            flash('کاربر عزیز، با این شماره موبایل قبلا ثبت نام شده، در صورت فراموشی رمز "فراموشی کلمه عبور" را لمس نمایید. ','danger')
            return redirect(url_for("login"))
        s.commit()      
        s.close()                           
    return render_template('signup.html')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        s = Session() 
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        user = s.query(User).filter(User.mobile == mobile).first()
        if user:
            good_sig = make_hashed_password(password)
            check_if_password_is_correct = hmac.compare_digest(good_sig, bytes(user.password , encoding= 'utf-8'))
            if  check_if_password_is_correct:
                session_f['user_id'] = user.id
                flash(f'{user.full_name}عزیز خوش آمدید.','success')                 
                return redirect(url_for("grades"))
            else:
                flash('رمز عبور خود را درست وارد نکرده اید!','danger')  
                return redirect(url_for("login"))
        else:
            flash('این نام کاربری قبلا ثبت نام نشده است!','danger')  
            return redirect(url_for("register"))
        s.commit()    
        s.close()                
    return render_template('login.html')
   

@app.route('/grades')     
def gradeSession():
    s = Session()
    user_id = 17
    all_courses = []
    courses = s.query(Course).all()
    if courses:
        for course in courses:
            lesson = s.query(Lesson).filter(Lesson.course_id == course.id).first()
            has_content = 'True' if lesson else 'False'
            all_courses.append({"id": course.id, "title":course.title, "image": course.image, "has_content": has_content})
    user = s.query(User).filter(User.id == user_id).first()
    len_user_purchased_lessons = 0
    if user and user.purchased_lessons:
        user_purchased_lessons = user.purchased_lessons.split(',')
        len_user_purchased_lessons = len(user_purchased_lessons)
    if len_user_purchased_lessons > 6 and user.grade == 'na':
        return redirect(url_for("information_completion_status")) 
    s.commit()
    s.close()     
    return  render_template('test_grades.html', all_courses = all_courses)

@app.route('/grade/<grade_id>')     
def grade(grade_id):
    s = Session()
    course_id = int(grade_id)
    user_id = 17
    all_lessons = []
    lessons = s.query(Lesson).filter(Lesson.course_id == course_id).all()
    user_purchased_lessons = s.query(User.purchased_lessons).filter(User.id == user_id).first()
    purchased_lessons_list = user_purchased_lessons[0].split(',')
    for lesson in lessons:
        show_lesson = 'True' if f'{lesson.id}' in purchased_lessons_list else 'False'
        all_lessons.append({"id": lesson.id, "title":lesson.title, "show_lesson":show_lesson}) 
    s.commit()
    s.close()        
    return  render_template('test_lessons.html', all_lessons = all_lessons)    

@app.route('/lesson/<lesson_id>')     
def status_question(lesson_id):
    lesson_id = int(lesson_id)
    user_id = 17
    has_access = check_user_access(user_id, lesson_id)
    if has_access:
        s = Session()
        has_new_question = s.query(Question).filter(Question.lesson_id == lesson_id).first()
        check_new_question = 'True' if has_new_question else 'False'
        enrol_user = s.query(Enrol_user.complete_question).filter(Enrol_user.lesson_id == lesson_id, Enrol_user.user_id == user_id).first()
        check_continue_previous_questions = 'False'
        if enrol_user and enrol_user[0] != 'True':
            check_continue_previous_questions = 'True'
        has_wrong_questions = s.query(User_answer.question_id).filter(User_answer.user_id == user_id, User_answer.ans_no == 1, User_answer.lesson_id == lesson_id).first()
        check_wrong_questions = 'True' if has_wrong_questions else 'False'
        s.commit()
        s.close() 
    else:
        flash('این درس برای شما باز نشده است!','danger')  
        return redirect(url_for("grade"))
    return render_template('test_train_type.html', new_question = check_new_question, previous_questions = check_continue_previous_questions, wrong_questions = check_wrong_questions, lesson_id = lesson_id) 
    
@app.route('/new-questions/<lesson_id>')
@app.route('/new-questions/<lesson_id>/<index>')     
def new_questions(lesson_id, index = 0): 
    page_name = 'new_questions'
    user_id = 17
    has_access = check_user_access(user_id, lesson_id)
    if has_access:
        s = Session()
        index = int(index)
        if index == -1 :
            all_previous_answer = s.query(User_answer).filter(User_answer.lesson_id == lesson_id, User_answer.user_id == user_id).all()
            if all_previous_answer:
                for answer in all_previous_answer:
                    s.delete(answer)
                    s.commit()
            has_user_enrol = s.query(Enrol_user).filter(Enrol_user.lesson_id == lesson_id, Enrol_user.user_id == user_id).first()          
            if has_user_enrol:
                s.query(Enrol_user).filter(Enrol_user.lesson_id == lesson_id, Enrol_user.user_id == user_id).update({ Enrol_user.complete_question: 'na' , Enrol_user.question_ids : 'na'})
                s.commit()
            else:
                enrol_user = Enrol_user(lesson_id = lesson_id, user_id=user_id, complete_question =  'na', question_ids = 'na')
                s.add(enrol_user)  
                s.commit()   
        user_enrol = s.query(Enrol_user).filter(Enrol_user.lesson_id == lesson_id, Enrol_user.user_id == user_id).first()             
        question_len = s.query(Question).filter(Question.lesson_id == lesson_id).count()
        if user_enrol.question_ids != 'na' :
            user_question_ids = user_enrol.question_ids.split(',')
            user_question_ids_len = len(user_question_ids)
        else:
            user_question_ids = [0]
            user_question_ids_len = 0
        next_new_question = 'na' 
        while user_question_ids_len + 1 < question_len:
            random_question = s.query(Question).order_by(func.rand()).filter(Question.lesson_id == lesson_id).first()
            if str(random_question.id) not in user_question_ids:
                next_new_question = random_question
                break    
        if next_new_question == 'na':
            first_question_id = s.query(Question.id).filter(Question.lesson_id == lesson_id).first()
            last_question_id = s.query(Question.id).order_by(Question.id.desc()).filter(Question.lesson_id == lesson_id).first()
            for id in range(int(first_question_id[0]), int(last_question_id[0])):
                if id not in user_question_ids:
                    next_new_question = s.query(Question).filter(Question.id == id).first()
                    break
        next_new_voice = s.query(Voice).filter(Voice.id == next_new_question.voice_id).first()
        next_new_answer = s.query(Answer).filter(Answer.question_id == next_new_question.id).first()
        lesson = s.query(Lesson).filter(Lesson.id == lesson_id).first()  
    else:
        flash('این درس برای شما باز نشده است!','danger')  
        return redirect(url_for("grade"))   
    question = next_new_question.text
    voice = f'{next_new_voice.path}' 
    question_id = next_new_question.id
    answer = next_new_answer.ans_text
    lesson_title = lesson.title
    s.commit()
    s.close() 
    return render_template('test_train.html', question = question, voice = voice, question_id = question_id, answer = answer, lesson_title = lesson_title, lesson_id = lesson_id, page_name = page_name)    

@app.route('/continue-questions/<lesson_id>')     
def continue_questions(lesson_id): 
    page_name = 'continue_questions'
    user_id = 17
    has_access = check_user_access(user_id, lesson_id)
    if has_access:
        s = Session()
        question_len = s.query(Question).filter(Question.lesson_id == lesson_id).count()
        user_enrol = s.query(Enrol_user).filter(Enrol_user.user_id== user_id, Enrol_user.lesson_id == lesson_id).first()
        if user_enrol.question_ids :
            user_question_ids = user_enrol.question_ids.split(',')
            user_question_ids_len = len(user_question_ids)
        else:
            user_question_ids = 'na'
            user_question_ids_len = 0
        next_continue_previous_question = 'na'     
        while user_question_ids_len + 1 < question_len:
            random_question = s.query(Question).order_by(func.rand()).filter(Question.lesson_id == lesson_id).first()
            if str(random_question.id) not in user_question_ids:
                next_continue_previous_question = random_question
                break   
        if next_continue_previous_question == 'na':
            first_question_id = s.query(Question.id).filter(Question.lesson_id == lesson_id).first()
            last_question_id = s.query(Question.id).order_by(Question.id.desc()).filter(Question.lesson_id == lesson_id).first()
            for id in range(int(first_question_id[0]), int(last_question_id[0])):
                if id not in user_question_ids:
                    next_continue_previous_question = s.query(Question).filter(Question.id == id).first()
                    break    
        next_continue_previous_voice = s.query(Voice).filter(Voice.id == next_continue_previous_question.voice_id).first()
        next_continue_previous_answer = s.query(Answer).filter(Answer.question_id == next_continue_previous_question.id).first()
        lesson = s.query(Lesson).filter(Lesson.id == lesson_id).first()
        question = next_continue_previous_question.text
        voice = f'{next_continue_previous_voice.path}'
        question_id = next_continue_previous_question.id
        answer = next_continue_previous_answer.ans_text
        lesson_title = lesson.title
        s.commit()
        s.close() 
    else:
        flash('این درس برای شما باز نشده است!','danger')  
        return redirect(url_for("grade"))     
    return render_template('test_train.html', question = question, voice = voice, question_id = question_id, answer = answer, lesson_title = lesson_title, lesson_id = lesson_id, page_name = page_name) 

@app.route('/wrong-questions/<lesson_id>/<index>')     
def wronge_questions(lesson_id, index): 
    page_name = 'wronge_questions'
    user_id = 17
    has_access = check_user_access(user_id, lesson_id)
    if has_access:
        s = Session()
        first_wrong_answer = s.query(User_answer).order_by(User_answer.question_id.asc()).filter(User_answer.user_id == user_id, User_answer.question_id> f'{index}', User_answer.ans_no == '1', User_answer.lesson_id == lesson_id).first()
        next_wrong_question = s.query(Question).filter(Question.id == first_wrong_answer.question_id).first()
        next_wrong_voice = s.query(Voice).filter(Voice.id == next_wrong_question.voice_id).first()
        next_wrong_answer = s.query(Answer).filter(Answer.question_id == next_wrong_question.id).first()
        lesson = s.query(Lesson).filter(Lesson.id == lesson_id).first()
        result = {"question":next_wrong_question.text, "voice": f'{next_wrong_voice.path}', "next_index": next_wrong_answer.question_id , "question_id": next_wrong_question.id, "answer": next_wrong_answer.ans_text,  "lesson_title":lesson.title}
        question = next_wrong_question.text 
        voice = f'{next_wrong_voice.path}' 
        question_id = next_wrong_question.id 
        answer = next_wrong_answer.ans_text 
        lesson_title = lesson.title
        s.commit()
        s.close() 
    else:
        flash('این درس برای شما باز نشده است!','danger')  
        return redirect(url_for("grade"))    
    return render_template('train.html', question = question, voice = voice, question_id = question_id, answer = answer, lesson_title = lesson_title, lesson_id = lesson_id, page_name = page_name)

@app.route('/ajax-set-user-answer', methods=['POST'])    
def user_answer():
    user_id = int(session_f['user_id']) 
    lesson_id = request.form.get('lesson_id')
    has_access = check_user_access(user_id, lesson_id)
    if has_access:
        question_id = request.form.get('question_id')
        ans_no = request.form.get('ans_no')
        question_type = request.form.get('question_type')
        s = Session()
        user_previous_answer  = s.query(User_answer.id).filter(User_answer.user_id == user_id, User_answer.question_id == question_id).first()
        if not user_previous_answer :
            user_answer = User_answer(ans_no=ans_no, user_id = user_id, question_id=question_id, lesson_id=lesson_id)
            s.add(user_answer)
            s.commit()
        else:
            user_answer_update = s.query(User_answer).filter(User_answer.id == user_previous_answer[0]).update({User_answer.ans_no : ans_no}) 
            s.commit()
        user_question_ids = s.query(Enrol_user.question_ids).filter(Enrol_user.lesson_id == lesson_id, Enrol_user.user_id == user_id).first()  
        if user_question_ids[0] != 'na':
            complete_user_question_ids = user_question_ids[0] + ',' + str(question_id)
            user_question_ids_len = len(user_question_ids[0].split(','))
        else:
            complete_user_question_ids = str(question_id)
            user_question_ids_len = 1 
        questions_len = s.query(Question).filter(Question.lesson_id == lesson_id).count() 
        if question_type == 1:
            next_content = False
            complete_question = 'True'
            if user_question_ids_len + 1 < questions_len:
                next_content = True
                complete_question = 'False' 
            s.query(Enrol_user).filter(Enrol_user.lesson_id == lesson_id, Enrol_user.user_id == user_id).update({ Enrol_user.complete_question: complete_question, Enrol_user.question_ids : complete_user_question_ids})
            s.commit()
            if next_content:
                s.commit()
                s.close()
                return redirect(url_for('new_questions', lesson_id=lesson_id))
        elif question_type == 2:
            complete_question = 'True'
            if user_question_ids_len + 1 < questions_len:
                next_content = True 
                complete_question = 'False' 
            s.query(Enrol_user).filter(Enrol_user.lesson_id == lesson_id, Enrol_user.user_id == user_id).update({ Enrol_user.complete_question: complete_question , Enrol_user.question_ids : complete_user_question_ids})
            s.commit()
            if next_content:
                s.commit()
                s.close()
                return redirect(url_for('continue_questions', lesson_id=lesson_id))
        else:
            return_fun = 'wronge_questions'
            next_content = s.query(User_answer).order_by(User_answer.question_id.asc()).filter(User_answer.user_id == user_id, User_answer.question_id> question_id, User_answer.ans_no == '1', User_answer.lesson_id == lesson_id).first()
            if next_content:
                s.commit()
                s.close()
                return redirect(url_for('wronge_questions', lesson_id=lesson_id, index = question_id))
        wrong_answer_no = s.query(func.count(User_answer.id)).order_by(User_answer.lesson_id).filter(User_answer.user_id == user_id ,User_answer.ans_no == '1', User_answer.lesson_id == lesson_id).scalar() 
        true_answer_no = s.query(func.count(User_answer.id)).order_by(User_answer.lesson_id).filter(User_answer.user_id == user_id,  User_answer.ans_no == '0', User_answer.lesson_id == lesson_id).scalar() 
        result = {"has_next_new_question":"False", "wrong_answer_no":wrong_answer_no, "true_answer_no":true_answer_no}    
        s.commit()
        s.close()
        return  jsonify(result)
    else:
        flash('این درس برای شما باز نشده است!','danger')  
        return redirect(url_for("grade"))  

@app.route('/zarinpal/<sale_plan_id>')
@app.route('/zarinpal/<sale_plan_id>/<course_id>')
def zarinpal( sale_plan_id, course_id = 0): 
    user_id = int(session_f['user_id']) 
    s = Session()
    ZARINPAL_WEBSERVICE  = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'
    MMERCHANT_ID = '46c993a0-9bed-11ea-8c18-000c295eb8fc'
    invoice_date= datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    client = Client(ZARINPAL_WEBSERVICE)
    sale_plan = s.query(Sale_plan).filter(Sale_plan.id == sale_plan_id).first()
    user = s.query(User).filter(User.id == user_id).first()
    if not (sale_plan or user):
        result = {"result":"user or sale plane id not found"}
        status_code = 401
    else:
        callback_url = f'{back_url}/zarinpal-callback' 
        result_zarinpal = client.service.PaymentRequest(MMERCHANT_ID,
                                           sale_plan.price,
                                           sale_plan.title,
                                           user.mobile,
                                           'tajbakhsh.ut.ac@gmail.com',
                                           callback_url)
        print(callback_url)                                   
        if result_zarinpal.Status == 100:
            if sale_plan_id == '2' : 
                lesson_ids = s.query(Lesson.id).filter(Lesson.course_id == course_id).all()
                str_lesson = ''
                for lesson_id in lesson_ids:
                    if str(lesson_id[0]) not in ['1','9','16','20','32','42']:
                        str_lesson = str_lesson +str(lesson_id[0]) + ","
                lessons = str_lesson[:-1]
            else:
                lessons = sale_plan.lessons        
            invoice = Invoice( invoice_no = result_zarinpal.Authority,  datetime = invoice_date , sale_plan_id = sale_plan_id, user_id = user_id, lessons = lessons, verify= -1)
            s.add(invoice)
            s.commit()
            s.close()
            zarinpal_url = f'https://www.zarinpal.com/pg/StartPay/{result_zarinpal.Authority}'
            s.commit()        
            s.close() 
            return redirect(zarinpal_url)
        else:
            flash('با عرض پوزش در هنگام اتصال به درگاه بانک خطایی رخ داده است!','danger')
            return redirect(url_for("confirm_purchase_information"))
    

@app.route('/zarinpal-callback')    
def zarinpal_callback():
    s = Session()
    ZARINPAL_WEBSERVICE  = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'    
    MMERCHANT_ID = '46c993a0-9bed-11ea-8c18-000c295eb8fc'
    print(MMERCHANT_ID)
    client = Client(ZARINPAL_WEBSERVICE)
    Status = request.args['Status'] 
    print(f'{Status}')
    Authority = request.args['Authority']
    if Status == 'OK':
        check_invoice = s.query(Invoice).filter(Invoice.invoice_no == Authority).first()
        if check_invoice:
            sale_plan = s.query(Sale_plan.price).filter(check_invoice.sale_plan_id == Sale_plan.id).first()
            result_zarinpal = client.service.PaymentVerification(MMERCHANT_ID,
                                                                Authority,
                                                                sale_plan[0])                                                                                                                                   
            if  result_zarinpal.Status == 100: 
                zarinpal_result_status = result_zarinpal.Status
                user = s.query(User).filter(User.id == check_invoice.user_id).first()
                result =  f'{user.full_name}عزیز پرداخت شما موفق بوده است.'
                type = 'success'
                status_code = 200 
                old_purchased_lessons = s.query(User.purchased_lessons).filter(User.id == check_invoice.user_id).first()
                new_purchased_lessons = check_invoice.lessons 
                new_purchased_lessons_split = new_purchased_lessons.split(',')
                old_purchased_lessons_split = old_purchased_lessons[0].split(',')
                purchased_lessons = old_purchased_lessons[0]
                for lesson in new_purchased_lessons_split:
                    if lesson not in old_purchased_lessons_split:
                        purchased_lessons = purchased_lessons  + ',' + lesson
                update_user = s.query(User).filter(User.id == check_invoice.user_id).update({User.purchased_lessons : purchased_lessons})  
                s.commit()
                #return 'Transaction success. RefID: ' + str(result.RefID)   
            elif result_zarinpal.Status == 101:
                zarinpal_result_status = result_zarinpal.Status
                user = s.query(User).filter(User.id == check_invoice.user_id).first()
                result =  f'{user.full_name}عزیز پرداخت شما موفق بوده است.'
                type = 'success'
                status_code = 200
                if check_invoice.sale_plan_id == 1:
                    purchased_lessons = check_invoice.lessons
                else : 
                    purchased_lessons_user = s.query(User.purchased_lessons).filter(User.id == check_invoice.user_id).first()
                    purchased_lessons = check_invoice.lessons + purchased_lessons_user[0] 
                update_user = s.query(User).filter(User.id == check_invoice.user_id).update({User.purchased_lessons : purchased_lessons})  
                s.commit()
                #return 'Transaction submitted : ' + str(result.Status)
            else:
                zarinpal_result_status = result_zarinpal.Status
                result =  'عملیات پرداخت ناموفق بود.'
                type = 'danger'
                #return 'Transaction failed. Status: ' + str(result.Status)
            invoice = s.query(Invoice).filter(Invoice.invoice_no == Authority).update({Invoice.status : zarinpal_result_status, Invoice.transaction_reference_id: result_zarinpal.RefID})       
    else:  
        invoice = s.query(Invoice).filter(Invoice.invoice_no == Authority).update({Invoice.status : Status})   
        s.commit()
        result =  'عملیات پرداخت ناموفق بود.'
        type = 'danger'
        #return 'Transaction failed or canceled by user'
    s.commit()
    s.close()
    flash(result, type)
    return redirect(url_for("grade"))
        
@app.route('/mobile/zarinpal-callback', methods=['GET',])
def api_pasargad_callback():
    s = Session()
    verify = request.form.get('verify')
    bills_status = s.query(Invoice.status).filter(Invoice.verify == verify).first()
    if bills_status:
        transactionID = bills_status[0]
    else:
        transactionID = None
    dict_data={"transaction" : transactionID}
    s.commit()
    s.close()
    return dict_data

@app.route('/information-completion-status' , methods=['GET','POST'])    
def information_completion_statuSession():
    if request.method =="POST":
        s = Session()
        user_id = session_f['user_id']
        grade = request.form.get('grade')
        city = request.form.get('city')
        user = s.query(User).filter(User.id == user_id).update({User.grade : grade, User.city : city})   
        s.commit()
        s.close()
        return redirect("grades")
    return render_template("Complete-info.html")

@app.route('/get-user-agent')    
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