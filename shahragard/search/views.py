from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from trip.models import Trip
from django.db.models import Q
from .serializers import TripSerializer
from json import loads, dumps


class SearchTrips(APIView):
    def post(self, request):
        userid = self.request.user.id
        request.data['user'] = userid
        start_time = request.data['start_time']
        origin = request.data['origin']
        destination = request.data['destination']
        car = request.data['car']
        query = Q()
        number_of_passengers = request.data['number_of_passengers']
        if start_time != '':
            query = query & Q(start_time=start_time)
        if origin != '':
            query = query & Q(origin=origin)
        if destination != '':
            query = query & Q(destination=destination)
        if car != '':
            query = query & Q(car=car)
        if number_of_passengers != '':
            query = query & Q(number_of_passengers=number_of_passengers)
        q = Trip.objects.filter(query)
        serializer = TripSerializer(q, many=True, context={
                                    "userid": request.user.id})
        return JsonResponse({'res': loads(dumps(serializer.data))},
                            status=status.HTTP_200_OK)
