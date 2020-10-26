from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Store
from .serializers import StoreSerializer
import requests


def validUser(user_uid):
    try:
        user_uid = str(user_uid)
        Store.objects.get(user_uid=user_uid)
        return True
    except ValidationError:
        return False


class StoreView(APIView):
    def get(self, request, user_uid):
        if request.method == 'GET':
            if validUser(user_uid):
                store = Store.objects.all()
                serializer = StoreSerializer(store, many=True)
                # r = requests.get('https://peaceful-shelf-78026.herokuapp.com/persons')
                # # persons = JSONParser().parse('https://peaceful-shelf-78026.herokuapp.com/persons')
                return JsonResponse(serializer.data, safe=False)
            else:
                return JsonResponse({'message': 'The tutorial does not exist or No Content'},
                                    status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse('', status=status.HTTP_405_METHOD_NOT_ALLOWED)
