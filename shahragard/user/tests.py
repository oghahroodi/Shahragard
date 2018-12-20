from user.models import Person, User
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from trip.models import RequestTrip, Trip


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

        user1 = User.objects.create(username="testuser", password="123123")
        user2 = User.objects.create(username="testuser2", password="123123")
        trip = Trip.objects.create(user=user1, start_time="110298",
                                   origin="تهران", destination="کرج", cost="1",
                                   number_of_passengers=2)
        requesttrip = RequestTrip.objects.create(user=user2, trip=trip,
                                                 number_of_passengers=1,
                                                 accept=False)

    def test_history_integeration(self):
        client = APIClient()
        response = client.get('/apiv1/history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_created_unit(self):
        try:
            a = User.objects.get(username="testuser")

            self.assert_("good")
        except:
            self.assert_("user and person unit test failed")

    def test_user_created_unit(self):
        try:
            a = RequestTrip.objects.get(username="testuser")
            self.assert_("good")

        except:
            self.assert_("history unit test failed")
