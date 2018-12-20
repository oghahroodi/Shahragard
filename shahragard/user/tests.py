from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase


class UserTestCase(TestCase):

    def test_signup_created(self):
        client = APIClient()
        response = client.post('/apiv1/user/', {
            "username": "usertest",
            "name": "user",
            "password": "1",
            "phone_number": "09123456754",
            "email": "test@test.com"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_invalidemail(self):
        client = APIClient()
        response = client.post('/apiv1/user/', {
            "username": "usertest",
            "name": "user",
            "password": "1",
            "phone_number": "09123456754",
            "email": "testtest.com"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalidphone(self):
        client = APIClient()
        response = client.post('/apiv1/user/', {
            "username": "usertest",
            "name": "user",
            "password": "1",
            "phone_number": "qq",
            "email": "test@test.com"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_emptyfield1(self):
        client = APIClient()
        response = client.post('/apiv1/user/', {
            "username": "",
            "name": "user",
            "password": "1",
            "phone_number": "qq",
            "email": "test@test.com"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_emptyfield2(self):
        client = APIClient()
        response = client.post('/apiv1/user/', {
            "username": "usertest",
            "name": "user",
            "password": "1",
            "phone_number": "",
            "email": ""
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
