import os
import json
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
        try:
            request.data['user'] = userid
            start_time = request.data['start_time']
            origin = request.data['origin']
            destination = request.data['destination']
            number_of_passengers = request.data['number_of_passengers']
        except:
            return JsonResponse({'status': 'give valid data'},
                                status=status.HTTP_400_BAD_REQUEST)
        if (len(request.data.get('start_time')) != 6 and
                len(request.data.get('start_time')) != 0):
            return JsonResponse(
                {'status': 'pls enter valid time'},
                status=status.HTTP_400_BAD_REQUEST)
        for i in request.data.get('start_time'):
            if not(i.isdigit()):
                return JsonResponse(
                    {'status': 'pls enter valid time'},
                    status=status.HTTP_400_BAD_REQUEST)
        f = open(os.path.dirname(__file__) + '/../../json_shahr.json').read()
        data = json.loads(f)
        tmp1 = False
        tmp2 = False
        if request.data['origin'] == '':
            tmp1 = True
        else:
            for i in data.values():
                if request.data['origin'] == i:
                    tmp1 = True
                    break
        if request.data['destination'] == '':
            tmp2 = True
        else:
            for i in data.values():
                if request.data['destination'] == i:
                    tmp2 = True
                    break
        if not(tmp1 and tmp2):
            return JsonResponse(
                {'status': 'pls enter valid city'},
                status=status.HTTP_400_BAD_REQUEST)
        query = Q()
        number_of_passengers = request.data['number_of_passengers']
        if start_time != '':
            query = query & Q(start_time=start_time)
        if origin != '':
            query = query & Q(origin=origin)
        if destination != '':
            query = query & Q(destination=destination)
        if number_of_passengers != '':
            query = query & Q(number_of_passengers=number_of_passengers)
        q = Trip.objects.filter(query)
        serializer = TripSerializer(q, many=True, context={
            "userid": request.user.id})
        return JsonResponse({'res': loads(dumps(serializer.data))},
                            status=status.HTTP_200_OK)
