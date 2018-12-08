from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from trip.models import RequestTrip

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


class RequestTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestTrip
        fields = ('start_time', 'origin', 'destination', 'cost')

        def get_start_time(self, obj):
            start_time = RequestTrip.objects.get(id=obj.trip.start_time)
            return start_time

        def get_origin(self, obj):
            origin = RequestTrip.objects.get(id=obj.trip.origin)
            return origin

        def get_destination(self, obj):
            destination = RequestTrip.objects.get(id=obj.trip.destination)
            return destination

        def get_number_of_passengers(self, obj):
            number_of_passengers = RequestTrip.objects.get(id=obj.trip.number_of_passengers)
            return number_of_passengers

