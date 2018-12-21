import os
import json
import redis
import string
import random
import binascii
import rollbar
import logging
from json import loads, dumps
from .serializers import *
from .models import Person
from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from rest_framework.permissions import AllowAny
from trip.models import Trip, RequestTrip
from user.const import Const

logger = logging.getLogger(__name__)

>>>>>>> shahragard/user/views.py

class Edit(APIView):
    def patch(self, request):
        try:
            email = request.data.get("email")
            name = request.data.get("name")
            car = request.data.get("car")
            plaque = request.data.get("plaque")
        except KeyError:
            rollbar.report_message("search key problem")
            return JsonResponse({'status': 'give valid data'},
                                status=status.HTTP_400_BAD_REQUEST)

        if plaque != '' and car != '':
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

            f = open(os.path.dirname(__file__) +
                     Const.mashin).read()

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
        logger.info("user with username : "+str(request.user.id)+" changed settings")
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

                try:
                    UserHandler.email(registerdata['email'], username)
                except redis.exceptions.ConnectionError:
                    rollbar.report_message("redis problem")
                    return JsonResponse(personserializer.errors,
                                        status=status.
                                        HTTP_503_SERVICE_UNAVAILABLE)
                logger.info("user with username : "+username+" created")
                return JsonResponse({'status': 'CREATED'},
                                    status=status.HTTP_201_CREATED)
            user.delete()
            rollbar.report_message("signup problem"+str(registerdata))
            return JsonResponse(personserializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        rollbar.report_message("signup problem"+str(registerdata))
        return JsonResponse(userserializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        userid = self.request.user.id
        request.data['user'] = userid
        person = Person.objects.get(user__id=userid)
        serializer = ProfilePageSerializer(person, context={"userid": userid})
        logger.info("userid : "+str(userid)+" seen profile page")
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
<<<<<<< shahragard/user/views.py
    red = redis.StrictRedis(host='localhost', port=6379,
                            password='', charset="utf-8",
                            decode_responses=True)
    info = red.hgetall(token)
    username = info.get('username')
    user = User.objects.get(username=username)
    user.is_active = True
    user.save()
    return HttpResponse("ایمیل با موفقیت تایید شد")


def get_suggestion_trips(user):
    qs1 = Trip.objects.values("origin", "destination")  # TODO: add active == True
    qs2 = RequestTrip.objects.filter(user=user).values("origin", "destination")
    return [dict(origin=i["origin"],destination=i["destination"]) for i in qs1.intersection(qs2)]


class SuggestionHandler(APIView):
    def get(self, request):
        return JsonResponse({"result": get_suggestion_trips(request.user)})
=======
    try:
        red = redis.StrictRedis(host='localhost', port=6379,
                                password='', charset="utf-8",
                                decode_responses=True)
        info = red.hgetall(token)
        username = info.get('username')
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()
        return HttpResponse("ایمیل با موفقیت تایید شد")
    except redis.exceptions.ConnectionError:
        return JsonResponse(personserializer.errors,
                            status=status.
                            HTTP_503_SERVICE_UNAVAILABLE)


class NotificationHandler(APIView):

    def get(self, request):
        userid = self.request.user.id
        notification = RequestTrip.objects.filter(trip__user__id=userid)
        # person = Person.objects.filter(user__id=userid)
        serializer = NotifSerializer(list(notification), many=True)
        resList = loads(dumps(serializer.data))
        # print(resList)
        return JsonResponse({"res": resList})


class HistoryHnadler(APIView):

    def get(self, request):
        userid = self.request.user.id
        history = RequestTrip.objects.filter(user__id=userid)
        serializer = HistorySerializer(list(history), many=True)
        resList = loads(dumps(serializer.data))
        rollbar.report_message("userid "+str(userid)+" got history")
        return JsonResponse({"res": resList})
>>>>>>> shahragard/user/views.py
