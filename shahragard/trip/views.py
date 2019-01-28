import json
import os.path
import logging
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from user.models import *
from user.models import User, Person
from django.http import JsonResponse
from .models import RequestTrip, Trip
from json import loads, dumps

# logger = logging.getLogger(__name__)


class TripHandler(APIView):

    def post(self, request, *args, **kwargs):
        userid = self.request.user.id
        if request.data.get('origin') == request.data.get('destination'):
            return JsonResponse(
                {'status': 'destination most different with origin'},
                status=status.HTTP_400_BAD_REQUEST)

        for i in request.data.get('start_time'):
            if not(i.isdigit()):
                return JsonResponse(
                    {'status': 'pls enter valid time'},
                    status=status.HTTP_400_BAD_REQUEST)

        if len(request.data.get('start_time')) != 6:
            return JsonResponse(
                {'status': 'pls enter valid time'},
                status=status.HTTP_400_BAD_REQUEST)

        for i in request.data['cost']:
            if not(i.isdigit()):
                return JsonResponse(
                    {'status': 'pls enter valid cost'},
                    status=status.HTTP_400_BAD_REQUEST)

        f = open(os.path.dirname(__file__) + '/../../json_shahr.json').read()
        data = json.loads(f)
        tmp1 = False
        tmp2 = False

        for i in data.values():
            if request.data['origin'] == i:
                tmp1 = True
                break

        for i in data.values():
            if request.data['destination'] == i:
                tmp2 = True
                break

        if not(tmp1 and tmp2):
            return JsonResponse(
                {'status': 'pls enter valid city'},
                status=status.HTTP_400_BAD_REQUEST)

        request.data['user'] = userid
        serializer = MakeTripSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status': 'CREATED'},
                                status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        userid = self.request.user.id
        request.data['user'] = userid
        serializer = RequestTripSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            # logger.info("userid : "+str(userid) +
            # " join to "+str(request.data['trip']))

            return JsonResponse({'status': 'CREATED'},
                                status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        userid = self.request.user.id
        tripid = request.data['trip']
        RequestTrip.objects.filter(user=userid, trip=tripid).delete()
        return JsonResponse({'status': 'DELETED'},
                            status=status.HTTP_202_ACCEPTED)


class CommentHandler(APIView):

    def post(self, request):
        tripid = request.data['trip']
        comment = Comment.objects.filter(trip=tripid)
        serializer = AllCommentSerializer(list(comment), many=True)
        resList = loads(dumps(serializer.data))
        return JsonResponse({"res": resList})

    def put(self, request):
        userid = self.request.user.id
        request.data['user'] = userid
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status': 'CREATED'},
                                status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
