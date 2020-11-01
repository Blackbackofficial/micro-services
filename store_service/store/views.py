from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .models import Store
import requests


# API
@api_view(['GET'])
def get_orders(request, user_uid):
    if validUser(user_uid):
        # Логика
        store_req = requests.get('http://127.0.0.1:8100/api/v1/orders/{}'.format(user_uid), json=request.data)
        filter_req = filter_response(store_req)
        return JsonResponse(filter_req, status=status.HTTP_200_OK, safe=False)
    return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_order(request, user_uid, order_uid):
    if validUser(user_uid):
        # Логика
        store_req = requests.get('http://127.0.0.1:8100/api/v1/orders/{user_uid}/{order_uid}'.format(
            user_uid=user_uid, order_uid=order_uid), json=request.data)
        store_req = filter_response(store_req)
        return JsonResponse(store_req, status=status.HTTP_200_OK, safe=False)
    return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def buy_order(request, user_uid):
    if validUser(user_uid):
        order_req = requests.post('http://127.0.0.1:8100/api/v1/orders/{}'.format(user_uid), json=request.data)
        order_req = order_req.json()
        response = JsonResponse(1, status=status.HTTP_201_CREATED, safe=False)
        response['Location'] = 'http://127.0.0.1:8100/api/v1/orders/{user_uid}/purchase/{order_uid}'.format(
            user_uid=user_uid, order_uid=order_req["orderUid"])
        return response
    return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def get_order_warranty(request, user_uid, order_uid):
    if validUser(user_uid):
        # Логика
        store = JSONParser().parse(request)
        store = store
    return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def get_order_refund(request, user_uid, order_uid):
    if validUser(user_uid):
        order_req = requests.delete('http://127.0.0.1:8100/api/v1/orders/{}'.format(order_uid), json=request.data)
        if order_req.status_code == 404:
            order_req = order_req.json()
            return JsonResponse(order_req, status=status.HTTP_404_NOT_FOUND, safe=False)
        return JsonResponse(1, status=status.HTTP_204_NO_CONTENT, safe=False)
    return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)


# Support function
def filter_response(store_req):
    store_req = store_req.json()
    if type(store_req) is dict:
        store_req['date'] = store_req['orderDate']
        del store_req['itemUid'], store_req['status'], store_req['orderDate']
    else:
        for item in store_req:
            item['date'] = item['orderDate']
            del item['itemUid'], item['status'], item['orderDate']
    return store_req


def validUser(user_uid):
    try:
        return Store.objects.get(user_uid=user_uid)
    except ValidationError:
        return False
