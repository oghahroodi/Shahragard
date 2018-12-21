from rest_framework import serializers
from .models import *
from user.models import User, Person


class MakeTripSerializer(serializers.ModelSerializer):

    def validate(self, data):
        userInstance = Person.objects.get(user__username=data['user'])
        if not(userInstance.hasCar()):
            raise serializers.ValidationError("nnn")

        return data

    class Meta:
        model = Trip
        fields = ('user', 'start_time', 'origin', 'destination', 'cost',
                  'number_of_passengers')


class RequestTripSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestTrip
        fields = ('user', 'trip', 'number_of_passengers',
                  'origin', 'destination')
