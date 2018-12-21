from rest_framework import serializers
from trip.models import Trip
from user.models import User


class TripSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = ('user', 'start_time', 'origin', 'destination',
                  'number_of_passengers', 'id')

    def get_user(self, obj):
        user = User.objects.get(id=obj.user.id)
        return user.username
