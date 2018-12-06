import binascii
import json
import redis
import string
import random
from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Person
from rest_framework.permissions import AllowAny


class UserHandler(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        registerdata = request.data.copy()
        userserializer = UserSerializer(
            data={"username": username, "password": password})
        if userserializer.is_valid():
            user = userserializer.save()
            userid = user.id
            user.set_password(password)
            user.is_active = False
            user.save()
            registerdata['user'] = userid
            personserializer = PersonSerializer(data=registerdata)
            if personserializer.is_valid():
                personserializer.save()
                UserHandler.email(registerdata['email'], username)
                return JsonResponse({'status': 'CREATED'},
                                    status=status.HTTP_201_CREATED)
            user.delete()
            return JsonResponse(personserializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(userserializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def email(receiver, username):
        red = redis.StrictRedis(
            host='localhost', port=6379, password='', charset="utf-8",
            decode_responses=True)
        random_token = ''.join([random.choice(
            string.ascii_uppercase + string.ascii_uppercase)
            for _ in range(50)])
        red.hmset(random_token, {"username": username})

        jsonDic = {'token': random_token, 'receiver': receiver}
        jsonStr = json.dumps(jsonDic)
        red.rpush('email', jsonStr)
