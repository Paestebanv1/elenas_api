from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
import requests
from getpass import getpass
from .models import Task


# Create your tests here.

class TestTasks(APITestCase):

    def authenticate(self):
        auth_endpoint = "http://localhost:8000/api_tasks/auth/" 
        username = input("What is your username?\n")
        password = getpass("What is your password?\n")
        json = {'username': username, 'password': password}
        auth_response = requests.post(auth_endpoint, json)
        token = auth_response.json()['token']
        global headers
        headers = {
            "Authorization": f"token {token}"
        }


    def test_creates_no_auth_tasks(self):
        sample_data = {
            "title" : "task6",
            "description" : "task6 descr",
            'date_start': '2015-11-09T23:55:59.342380Z', 
            'date_end': '2015-11-09T23:55:59.342380Z', 
            'location': "casa"
        }
        response = self.client.post(reverse('create_tasks'), sample_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_list_tasks(self):
        endpoint = "http://127.0.0.1:8000/api_tasks/list/"
        get_response = requests.get(endpoint, headers=headers) 
        data = get_response.json()
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)


    def test_creates_tasks(self):
        sample_data = {
            "title" : "task6",
            "description" : "task6 descr",
            'date_start': '2015-11-09T23:55:59.342380Z', 
            'date_end': '2015-11-09T23:55:59.342380Z', 
            'location': "casa"
        }
        endpoint = "http://127.0.0.1:8000/api_tasks/"
        get_response = requests.post(endpoint, json=sample_data, headers=headers) 
        self.assertEqual(get_response.status_code, status.HTTP_201_CREATED)


    def test_creates_incomplete_tasks(self):
        sample_data = {
            "description" : "task6 descr",
            'date_start': '2015-11-09T23:55:59.342380Z', 
            'date_end': '2015-11-09T23:55:59.342380Z', 
            'location': "casa"
        }
        endpoint = "http://127.0.0.1:8000/api_tasks/"
        get_response = requests.post(endpoint, json=sample_data, headers=headers) 
        self.assertEqual(get_response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_creates_bad_option_tasks(self):
        sample_data = {
            "title" : "task6",
            "description" : "task6 descr",
            'date_start': '2015-11-09T23:55:59.342380Z', 
            'date_end': '2015-11-09T23:55:59.342380Z', 
            'location': "casa",
            'status' : 'NT'
        }
        endpoint = "http://127.0.0.1:8000/api_tasks/"
        get_response = requests.post(endpoint, json=sample_data, headers=headers) 
        self.assertEqual(get_response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_tasks(self):
        sample_data_create = {
            "title" : "task6",
            "description" : "task6 descr",
            'date_start': '2015-11-09T23:55:59.342380Z', 
            'date_end': '2015-11-09T23:55:59.342380Z', 
            'location': "casa"
        }
        endpoint = "http://127.0.0.1:8000/api_tasks/"
        get_response = requests.post(endpoint, json=sample_data_create, headers=headers) 
        data = get_response.json()

        sample_data = {
            "title" : "task modified",
            "description" : "task x modified",
            'date_start': '2022-11-09T23:55:59.342380Z', 
            'date_end': '2022-11-09T23:55:59.342380Z', 
            'location': "casa"
        }
        endpoint = f"http://127.0.0.1:8000/api_tasks/{data['id']}/update"
        get_response = requests.put(endpoint, json=sample_data, headers=headers) 
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)


    def test_bad_update_tasks(self):
        sample_data_create = {
            "title" : "task6",
            "description" : "task6 descr",
            'date_start': '2015-11-09T23:55:59.342380Z', 
            'date_end': '2015-11-09T23:55:59.342380Z', 
            'location': "casa"
        }
        endpoint = "http://127.0.0.1:8000/api_tasks/"
        get_response = requests.post(endpoint, json=sample_data_create, headers=headers) 
        data = get_response.json()

        sample_data = {
            "title" : "task modified",
            "description" : "task x modified",
            'date_start': '2022-11-09T23:55:59.342380Z', 
            'date_end': '2022-11-09T23:55:59.342380Z', 
            'location': "casa",
            'status' : 'NT'
        }
        endpoint = f"http://127.0.0.1:8000/api_tasks/{data['id']}/update"
        get_response = requests.put(endpoint, json=sample_data, headers=headers) 
        self.assertEqual(get_response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_no_existing_update_tasks(self):
        sample_data = {
            "title" : "task modified",
            "description" : "task x modified",
            'date_start': '2022-11-09T23:55:59.342380Z', 
            'date_end': '2022-11-09T23:55:59.342380Z', 
            'location': "casa",
            'status' : 'NT'
        }
        endpoint = "http://127.0.0.1:8000/api_tasks/999/update"
        get_response = requests.put(endpoint, json=sample_data, headers=headers) 
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_tasks(self):
        endpoint_count = "http://127.0.0.1:8000/api_tasks/list/"
        get_response_count = requests.get(endpoint_count, headers=headers) 
        data = get_response_count.json()
        endpoint = f"http://127.0.0.1:8000/api_tasks/{data['results'][0]['id']}/delete"
        get_response = requests.delete(endpoint, headers=headers) 
        self.assertEqual(get_response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_no_existing_tasks(self):
        endpoint = f"http://127.0.0.1:8000/api_tasks/999/delete"
        get_response = requests.delete(endpoint, headers=headers) 
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)


    def test_wrong_method(self):
        endpoint = f"http://127.0.0.1:8000/api_tasks/999/delete"
        get_response = requests.put(endpoint, headers=headers) 
        self.assertEqual(get_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_good_search_method(self):
        endpoint = f"http://127.0.0.1:8000/api_tasks/search/?q=t"
        get_response = requests.get(endpoint, headers=headers) 
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)


    def test_bad_search_method(self):
        self.authenticate()      
        endpoint = f"http://127.0.0.1:8000/api_tasks/search/?q=pqpqpq"
        get_response = requests.get(endpoint, headers=headers) 
        data = get_response.json()
        self.assertEqual(data['count'], 0)


    def test_detail_method(self):
        endpoint_count = "http://127.0.0.1:8000/api_tasks/list/"
        get_response_count = requests.get(endpoint_count, headers=headers) 
        data = get_response_count.json()
        endpoint = f"http://127.0.0.1:8000/api_tasks/{data['results'][0]['id']}"
        get_response = requests.get(endpoint, headers=headers) 
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_detail_no_existing_method(self):
        endpoint = f"http://127.0.0.1:8000/api_tasks/9999"
        get_response = requests.get(endpoint, headers=headers) 
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)


    def test_detail_foreign_method(self):
        endpoint = f"http://127.0.0.1:8000/api_tasks/22"
        get_response = requests.get(endpoint, headers=headers) 
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)