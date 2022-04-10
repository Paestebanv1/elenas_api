import requests
from getpass import getpass

auth_endpoint = "http://localhost:8000/api_tasks/auth/" 
username = input("What is your username?\n")
password = getpass("What is your password?\n")
json = {'username': username, 'password': password}
auth_response = requests.post(auth_endpoint, json) 
print(auth_response.json())

if auth_response.status_code == 200:
    token = auth_response.json()['token']

    headers = {
        "Authorization": f"token {token}"
    }
    endpoint = "http://127.0.0.1:8000/api_tasks/list/"

    get_response = requests.get(endpoint, headers=headers) 
    
    data = get_response.json()
    next_url = data['next']
    results = data['results']
    print("next_url", next_url)
    print(results)