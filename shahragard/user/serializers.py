from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('user', 'name', 'phone_number', 'email')
