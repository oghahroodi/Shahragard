from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Person


class Edit(APIView):
    def patch(self, request):
        email = request.data.get("email")
        name = request.data.get("name")
        car = request.data.get("car")
        plaque = request.data.get("plaque")
        person = Person.objects.get(user__id=request.user.id)
        person.name = name
        person.email = email
        person.car = car
        person.plaque = plaque
        person.save()
        return JsonResponse({"status": "200"})
