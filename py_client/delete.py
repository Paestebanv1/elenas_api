from itertools import product
import requests

task_id = input("What is the task id you want to delete? ")


try:
    task_id = int(task_id)
except:
    task_id = None
    print(f'{task_id} not a valid id')

if task_id:
    endpoint = f"http://127.0.0.1:8000/api_tasks/{task_id}/delete"

    get_response = requests.delete(endpoint)
    print(get_response.status_code, get_response.status_code==204)
