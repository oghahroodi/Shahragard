import re
from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from trip.models import RequestTrip, Trip
from trip.serializers import MakeTripSerializer
from json import loads, dumps
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


class NotifSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    tripData = serializers.SerializerMethodField()

    class Meta:
        model = RequestTrip
        fields = ('user', 'trip', 'number_of_passengers', 'tripData')

    def get_user(self, obj):
        user = User.objects.get(id=obj.user.id)
        return user.username

    def get_tripData(self, obj):
        trip = Trip.objects.filter(id=obj.trip.id)
        serializer = MakeTripSerializer(list(trip), many=True)
        resList = loads(dumps(serializer.data))
        # print(resList)
        return ({"trip": resList})


class HistorySerializer(serializers.ModelSerializer):
    tripData = serializers.SerializerMethodField()

    class Meta:
        model = RequestTrip
        fields = ('user', 'trip', 'number_of_passengers', 'accept', 'tripData')

    def get_tripData(self, obj):
        trip = Trip.objects.filter(id=obj.trip.id)
        serializer = MakeTripSerializer(list(trip), many=True)
        resList = loads(dumps(serializer.data))
        return ({"trip": resList})


class SugesstionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SuggetionFeature
        fields = ('user', 'mashhad', 'tehran', 'karaj', 'shiraz', 'qom',
                  'search_origin_count', 'search_des_count', 'make_trip_count')
