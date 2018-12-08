import os
import json
import redis
import string
import random
import binascii
from .serializers import *
from .models import Person
from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from rest_framework.permissions import AllowAny
from trip.models import RequestTrip
from django.db.models import Q



class Edit(APIView):
    def patch(self, request):
        email = request.data.get("email")
        name = request.data.get("name")
        car = request.data.get("car")
        plaque = request.data.get("plaque")
        if len(plaque) != 6:
            return JsonResponse({"status": "pls enter valid plaque"},
                                status=status.HTTP_400_BAD_REQUEST)
        for i in range(len(plaque)-1, -1, -1):
            if i != 3:
                if not(plaque[i].isdigit()):
                    return JsonResponse({"status": "pls enter valid plaque"},
                                        status=status.HTTP_400_BAD_REQUEST)
            else:
                if plaque[i].isdigit():
                    return JsonResponse({"status": "pls enter valid plaque"},
                                        status=status.HTTP_400_BAD_REQUEST)

        f = open(os.path.dirname(__file__) + '/../../json_mashin.json').read()
        data = json.loads(f)
        tmp = False
        for i in data.keys():
            if car == i:
                tmp = True
                break
        if not tmp:
            return JsonResponse({"status": "pls enter valid machine"},
                                status=status.HTTP_400_BAD_REQUEST)
        person = Person.objects.get(user__id=request.user.id)
        if name != '':
            person.name = name
        if email != '':
            person.email = email
        if car != '':
            person.car = car
        if plaque != '':
            person.plaque = plaque
        person.save()
        return JsonResponse({"status": "200"})


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

    def get(self, request):
        userid = self.request.user.id
        request.data['user'] = userid
        person = Person.objects.get(user__id=userid)
        serializer = ProfilePageSerializer(person, context={"userid": userid})
        return JsonResponse(serializer.data)

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


def validation(request, token):
    red = redis.StrictRedis(host='localhost', port=6379,
                            password='', charset="utf-8",
                            decode_responses=True)
    info = red.hgetall(token)
    username = info.get('username')
    user = User.objects.get(username=username)
    user.is_active = True
    user.save()
    return HttpResponse("ایمیل با موفقیت تایید شد")


class historyHandler(APIView):

    def get(self, request):
        userid = self.request.user.id
        query = Q()
        query = Q(user_id=userid)
        q = RequestTrip.objects.filter(query)
        serializer = RequestTripSerializer(q, many=True, context={
            "userid": request.user.id})
        return JsonResponse({'res': loads(dumps(serializer.data))}, status=status.HTTP_200_OK)

    