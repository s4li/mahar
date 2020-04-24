import requests, json

if __name__ == "__main__":
    url ='http://localhost:5000/api/home'
    data = {
            'mobile' : '09196410501',
            'password' : '13751123p'
    }
    #response = requests.post(url, json= json.dumps(data))
    response = requests.get(url)
    print(response.status_code)