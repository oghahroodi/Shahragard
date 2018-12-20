from rest_framework import serializers
from trip.models import Trip
from user.models import User


class TripSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = ('user', 'username', 'start_time', 'origin', 'destination',
                  'number_of_passengers', 'id')

    def get_username(self, obj):
        user = User.objects.get(id=obj.user.id)
        return user.username
