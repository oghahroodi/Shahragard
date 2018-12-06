from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from user.models import *
from user.models import User, Person
from django.http import JsonResponse


class TripHandler(APIView):

    def post(self, request, *args, **kwargs):
        userid = self.request.user.id
        request.data['user'] = userid
        serializer = MakeTripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status': 'CREATED'},
                                status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
