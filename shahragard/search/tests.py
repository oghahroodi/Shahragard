from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase, Client
from user.models import User
from rest_framework.test import force_authenticate


class SearchTestCase(TestCase):

    # def test_search_all_integeration(self):
    #     user = User.objects.create(username='testuser')
    #     user.set_password('12345')
    #     user.save()
    #     user = User.objects.get(username='testuser')
    #     c = Client()
    #     response = c.post('/apiv1/search/', {
    #         "start_time": "",
    #         "origin": "",
    #         "destination": "",
    #         "number_of_passengers": ""
    #     },
    #         format='json')
    #     force_authenticate(response, user=user)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signup_badinput1_integeration(self):
        client = APIClient()
        response = client.post('/apiv1/search/', {
            "start_time": "salam",
            "origin": "",
            "destination": "",
            "number_of_passengers": ""
        },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_badinput2_integeration(self):
        client = APIClient()
        response = client.post('/apiv1/search/', {
            "start_time": "",
            "origin": "123",
            "destination": "123",
            "number_of_passengers": ""
        },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_badinput3_integeration(self):
        client = APIClient()
        response = client.post('/apiv1/search/', {
            "start_time": "",
            "origin": "",
            "destination": "",
            "number_of_passengers": "salam"
        },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
