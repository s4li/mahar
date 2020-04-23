from flask import Flask, jsonify, request
from flask_cors import CORS
from Back.models import session, User
from datetime import datetime, timedelta
import jwt, json

app = Flask(__name__)
app.secret_key = 'parastu'

# enable CORS
CORS(app)

@app.route('/api/register', methods=('POST',))
def register():
    json_data = request.get_json()
    data = json.loads(json_data)
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
        response = {'result':'success', 'full_name': user.full_name, 'token':token.decode('UTF-8')}
    else:
        response = {'result':'user_exists'}
        status_code = 401
    session.close()                          
    return jsonify(response), status_code


if __name__ == '__main__':
    app.run()