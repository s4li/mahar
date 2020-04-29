from flask import Flask, jsonify, request
from flask_cors import CORS
from functools import wraps
from .models import session, User, Course, Lesson
from datetime import datetime, timedelta
import jwt, json

app = Flask(__name__)
app.secret_key = 'mahar'

# enable CORS
CORS(app)


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
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
    #j_data = request.get_json()
    #data = json.loads(j_data)
    data = request.get_json()
    user = session.query(User).filter(User.mobile == data['mobile']).first()
    session.commit()
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
    session.commit()     
    session.close()             
    return jsonify(response), status_code

@app.route('/api/get-user-information')
@token_required
def user_information(cuser):
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
    all_courses = []
    courses = session.query(Course)
    for course in courses:
        lesson = session.query(Lesson).filter(Lesson.course_id == course.id).first()
        has_content = True if lesson else False
        all_courses.append({"id": course.id, "title":course.title, "has_content": has_content})
    session.commit()    
    session.close() 
    return jsonify(all_courses)

@app.route('/api/lessens')     
@token_required
def lessons(cuser):
    course_id = int(request.args['course_id'])
    user_id = int(request.args['user_id'])
    all_lessons = []
    lessons = session.query(Lesson).filter(Lesson.course_id == course_id)
    session.commit() 
    user_purchased_lessons = session.query(User.purchased_lessons).filter(User.id == user_id).first()
    purchased_lessons = user_purchased_lessons.split(',')
    for lesson in lessons:
        show_lesson = True if lesson.id in purchased_lessons else False
        all_lessons.append({"id": lesson.id, "title":lesson.title, "show_lesson":show_lesson})   
    session.close() 
    return jsonify(all_lessons)    

if __name__ == '__main__':
    app.run(debug=True)