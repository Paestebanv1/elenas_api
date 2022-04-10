import requests

endpoint = "http://127.0.0.1:8000/api_tasks/10/update"

data = {
    "title" : "taskx",
    "owner" : 1234,
    "description" : "task6 descrx"
 #   'date_start': '2015-11-09T23:55:59.342380Z', 
 #   'date_end': '2015-11-09T23:55:59.342380Z', 
 #   'location': "casa"
}

get_response = requests.put(endpoint, json=data)
print(get_response.json())
