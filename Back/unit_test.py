import requests

BASE_URL = 'http://localhost:8080'
BACK_URL = 'http://localhost:5555'

def test_home_get_method():
    url = f'{BASE_URL}/'
    response = requests.get(url)
    if not (response and response.status_code == 200 and  'alert-danger' not in response.text and 'alert-dismissible' not in response.text): 
        print(f'Error, There is a problem to get home page.\nresponse.status_code = {response.status_code}')
        return False, response   
    return True, response

def test_login_get_method():   
    url = f'{BASE_URL}/login'
    response = requests.get(url)
    if not (response and response.status_code == 200 and  'alert-danger' not in response.text and 'alert-dismissible' not in response.text):
        print(f'Error, There is a problem to get login page.\n response.status_code = {response.status_code}')
        return False, response
    return True, response 

def test_login_post_method():
    url = f'{BACK_URL}/api/login'
    data = {
        'mobile'  :  '09200000000',
        'password':  'unit_test'
    }    
    response = requests.post(url, json= data)
    if not (response and response.status_code == 200 and  'alert-danger' not in response.text and 'alert-dismissible' not in response.text and 'alert-validate' not in response.text):
        print(f'Error, There is a problem to post login .\n response.status_code = {response.status_code}')
        return False, response
    return True, response

def test_user_login_process():
    is_passed, response = test_home_get_method()
    if is_passed == False:
        return False , response   
    is_passed, response= test_login_get_method()
    if is_passed == False:
        return False, response 
    is_passed, response= test_login_post_method( ) 
    if is_passed == False:
        return False , response   
    return True, response 

def test_courses_get_method(user_id, token):
    url = f'{BACK_URL}/api/courses'
    headers = {'Authorization':f'Bearer: {token}'}
    params = {'user_id':user_id}
    response = requests.get(url, headers= headers, params= params)
    if not (response and response.status_code == 200):
        print(f'Error, There is a problem to get grade page.\n response.status_code = {response.status_code}')
        return False, response     
    return True, response 

def test_course_content_get_method(course_id, user_id, token):
    url = f'{BACK_URL}/api/lessons'
    headers = {'Authorization':f'Bearer: {token}'}
    params = {'course_id':course_id, 'user_id':user_id}
    response = requests.get(url, headers= headers, params= params)
    if not (response and response.status_code == 200):
        print(f'Error, There is a problem to get course content page.\n response.status_code = {response.status_code}')
        return False, response     
    return True, response 

def test_lesson_content_get_method(lesson_id, user_id, token, print_error = False):
    url = f'{BACK_URL}/api/get-status-question-user'
    headers = {'Authorization':f'Bearer: {token}'}
    params = {'lesson_id':lesson_id, 'user_id':user_id}
    response = requests.get(url, headers= headers, params= params)
    if not (response and response.status_code == 200):
        if print_error:
            print(f'Error, There is a problem to get lesson content page.\n response.status_code = {response.status_code}')
        return False, response     
    return True, response 

def find_target_lesson(courses, free_lesson = False):
    target_lesson = None
    if free_lesson:
        for i in range(len(courses)):
            lesson_id = courses[i]['id']
            is_passed, response = test_lesson_content_get_method(lesson_id, user_id, token)
            if response and response.status_code == 200 and is_passed == True:
                target_lesson = courses[i]
                break
    else:            
        for i in range(len(courses)):
            lesson_id = courses[i]['id']
            is_passed, response = test_lesson_content_get_method(lesson_id, user_id, token)
            if response.status_code != 200 and is_passed == False:
                target_lesson = courses[i]
                break
    return target_lesson

def test_zarinpal_get_method(user_id, course_id, token):
    type_conction = 'site'
    sale_plan_id = '1'
    url = f'{BACK_URL}/api/zarinpal/{type}/{user_id}/{sale_plan_id}/{course_id}'
    headers = {'Authorization':f'Bearer: {token}'}
    response = requests.get(url, headers= headers)
    if not (response and response.status_code == 200):
        print(f'Error, There is a problem to get lesson content page.\n response.status_code = {response.status_code}')
        return False, response     
    return True, response  

def test_choice_lesson_process(user_id, token):
    is_passed, response = test_courses_get_method(user_id, token)
    if is_passed == False:
        return False, response  
    json_result = response.json() 
    if not (json_result.get('all_courses') and len(json_result) > 0): 
        print ('Error, There is a problem to get all_courses and complete_information from get grade page.')
        return False, response   
    all_courses = json_result['all_courses']  
    complete_information = json_result['complete_information']
    first_course_id = all_courses[0]['id']
    is_passed, response = test_course_content_get_method(first_course_id, user_id, token) 
    if is_passed == False:
        return False, response 
    json_result = response.json()
    free_lesson = find_target_lesson(json_result, free_lesson = True)
    if free_lesson == None:
        print(f'Error, There is a problem to find free lesson content page.')
        return False, response 
    is_passed, response = test_lesson_content_get_method( free_lesson['id'], user_id, token, True)
    if is_passed == False:
        print(f'Error, There is a problem to get free lesson content page.\n response.status_code = {response.status_code}')
        return False, response 
    premium_lesson = find_target_lesson(json_result, free_lesson = False) 
    if premium_lesson == None:
        print(f'Error, There is a problem to find premium lesson content page.')
        return False, response  
    is_passed, response_premium_lesson = test_zarinpal_get_method(premium_lesson['id'], user_id, token)
    if is_passed == False:
        print(f'Error, There is a problem to get zarinpal page.\n response.status_code = {response.status_code}')
        return False, response      
    return True, response



def test_content_lesson_process(user_id, token):
    return True, response


if __name__ == "__main__":
    is_passed, response = test_user_login_process() 
    json_result = response.json()
    if is_passed == True:
        print('Login process is successful.')
        if not (json_result.get('id') and json_result.get('token')): 
            print ('Error, There is a problem to get cookies and user_id from post login page.')
        token = json_result['token']
        user_id = json_result['id']
        is_passed, response = test_choice_lesson_process(user_id, token)
        if is_passed == True:
            print('Choice choice lesson is successful.')
            is_passed, response = test_content_lesson_process(user_id, token)
        else:
            print('Choice choice courses is failed!')    
    else:
        print('Login process is failed!')