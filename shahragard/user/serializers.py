from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from trip.models import RequestTrip, Trip
from trip.serializers import MakeTripSerializer
from json import loads, dumps


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')


class PersonSerializer(serializers.ModelSerializer):

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
        print(resList)
        return ({"trip": resList})
