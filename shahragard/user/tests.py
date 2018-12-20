from user.models import Person, User
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase


class UserTestCase(TestCase):

    def test_signup_created_integeration(self):
        client = APIClient()
        response = client.post('/apiv1/user/', {
            "username": "usertest",
            "name": "user",
            "password": "1",
            "phone_number": "09123456754",
            "email": "test@test.com"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_invalidemail_integeration(self):
        client = APIClient()
        response = client.post('/apiv1/user/', {
            "username": "usertest",
            "name": "user",
            "password": "1",
            "phone_number": "09123456754",
            "email": "testtest.com"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalidphone_integeration(self):
        client = APIClient()
        response = client.post('/apiv1/user/', {
            "username": "usertest",
            "name": "user",
            "password": "1",
            "phone_number": "qq",
            "email": "test@test.com"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_emptyfield1_integeration(self):
        client = APIClient()
        response = client.post('/apiv1/user/', {
            "username": "",
            "name": "user",
            "password": "1",
            "phone_number": "qq",
            "email": "test@test.com"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_emptyfield2_integeration(self):
        client = APIClient()
        response = client.post('/apiv1/user/', {
            "username": "usertest",
            "name": "user",
            "password": "1",
            "phone_number": "",
            "email": ""
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_profilepage_integeration(self):
    #     client = APIClient()
    #     response = client.post('/apiv1/user/', {
    #         "username": "usertest",
    #         "name": "user",
    #         "password": "1",
    #         "phone_number": "09123456754",
    #         "email": "test@test.com"
    #     }, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     client.login(username='usertest', password='1')

    #     response = client.get('/apiv1/user/')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def setUp(self):

        User.objects.create(username="testuser", password="123123")

    def test_user_created_unit(self):
        try:
            a = User.objects.get(username="testuser")

        except:
            self.assert_("user and person unit test failed")
