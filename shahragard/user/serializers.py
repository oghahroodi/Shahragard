import re
from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class UserSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if len(data['username']) > 10 ** 3:
            raise serializers.ValidationError("buffer overflow attack")
        return data

    class Meta:
        model = User
        fields = ('username', 'password')


class PersonSerializer(serializers.ModelSerializer):

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    def validate(self, data):
        if len(data['name']) > 10 ** 3:
            raise serializers.ValidationError("buffer overflow attack")
        if len(data['phone_number']) > 10 ** 3:
            raise serializers.ValidationError("buffer overflow attack")
        if len(data['email']) > 10 ** 3:
            raise serializers.ValidationError("buffer overflow attack")

        pattern = re.compile("[^@]+@[^@]+\.[^@]+")
        if not(pattern.match(data['email'])):
            raise serializers.ValidationError({
                "email": [
                    "فرمت ایمیل اشتباه است."
                ]
            })

        if (len(data['phone_number']) != 11 or
                not (PersonSerializer.is_number(data['phone_number']))):
            raise serializers.ValidationError({
                "phone_number": [
                    "شماره تلفن باید عدد و بین 10 تا 11 رقم باشد."
                ]
            })

        return data

    class Meta:
        model = Person
        fields = ('user', 'name', 'phone_number', 'email')


class ProfilePageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('user', 'name', 'phone_number', 'email', 'car', 'plaque')
