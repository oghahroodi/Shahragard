from django.db import models
from user.models import User


class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.CharField(max_length=50, null=False)
    origin = models.CharField(max_length=50, null=False)
    destination = models.CharField(max_length=50, null=False)
    cost = models.CharField(max_length=50, null=False)
    number_of_passengers = models.IntegerField(null=False)


class RequestTrip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    accept = models.BooleanField(default=False)
    number_of_passengers = models.IntegerField(null=False)