from rest_framework import serializers
from .models import *


class MakeTripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = ('user', 'start_time', 'origin', 'destination', 'cost',
                  'number_of_passengers')
