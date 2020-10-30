from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
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


@api_view(['GET'])
def get_orders(request, user_uid):
    if request.method == 'GET':
        if validUser(user_uid):
            # Логика
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


@api_view(['POST'])
def buy_order(request, user_uid):
    if request.method == 'POST':
        if validUser(user_uid):
            # Логика
            store = request.data
            req = requests.post('http://127.0.0.1:8100/api/v1/orders/{}'.format(user_uid), json=store)
            req = req.json()
            response = JsonResponse(1, status=status.HTTP_201_CREATED, safe=False)
            response['Location'] = 'http://127.0.0.1:8100/api/v1/orders/{user_uid}/purchase/{order_uid}'.format(
                user_uid=user_uid, order_uid=req["orderUid"])
            return response
        else:
            return JsonResponse({'message': 'The tutorial does not exist or No Content'},
                                status=status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse('', status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_order(request, user_uid, order_uid):
    if request.method == 'GET':
        if validUser(user_uid):
            # Логика
            store = JSONParser().parse(request)
            store = store
        else:
            return JsonResponse({'message': 'The tutorial does not exist or No Content'},
                                status=status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse('', status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def get_order_warranty(request, user_uid, order_uid):
    if request.method == 'POST':
        if validUser(user_uid):
            # Логика
            store = JSONParser().parse(request)
            store = store
        else:
            return JsonResponse({'message': 'The tutorial does not exist or No Content'},
                                status=status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse('', status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Только метод DELETE
@api_view(['POST'])
def get_order_refund(request, user_uid, order_uid):
    if request.method == 'POST':
        if validUser(user_uid):
            # Логика
            store = JSONParser().parse(request)
            store = store
        else:
            return JsonResponse({'message': 'The tutorial does not exist or No Content'},
                                status=status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse('', status=status.HTTP_405_METHOD_NOT_ALLOWED)
