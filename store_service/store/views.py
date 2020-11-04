from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Store
import requests


# API
@api_view(['GET'])
def get_orders(request, user_uid):
    if validUser(user_uid):
        storeReq = requests.get('http://127.0.0.1:8100/api/v1/orders/{}'.format(user_uid)).json()
        for item in storeReq:
            warrantyResp = requests.get('http://127.0.0.1:8200/api/v1/warranty/{}'.format(item['itemUid'])).json()
            warehouseResp = requests.get('http://127.0.0.1:8300/api/v1/warehouse/{}'.format(item['itemUid'])).json()
            item.update(warrantyResp, **warehouseResp)
        storeReq = filter_response(storeReq)
        return JsonResponse(storeReq, status=status.HTTP_200_OK, safe=False)
    return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_order(request, user_uid, order_uid):
    if validUser(user_uid):
        storeReq = requests.get('http://127.0.0.1:8100/api/v1/orders/{user_uid}/{order_uid}'.format(
            user_uid=user_uid, order_uid=order_uid)).json()
        warrantyResp = requests.get('http://127.0.0.1:8200/api/v1/warranty/{}'.format(storeReq['itemUid'])).json()
        warehouseResp = requests.get('http://127.0.0.1:8300/api/v1/warehouse/{}'.format(storeReq['itemUid'])).json()
        storeReq.update(warrantyResp, **warehouseResp)  # через дополнительные параметры конструктора типа
        storeReq = filter_response(storeReq)
        return JsonResponse(storeReq, status=status.HTTP_200_OK)
    return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def purchase_order(request, user_uid):
    if validUser(user_uid):
        orderResp = requests.post('http://127.0.0.1:8100/api/v1/orders/{}'.format(user_uid), json=request.data)
        if orderResp.status_code == 200:
            orderResp = orderResp.json()
            response = JsonResponse(1, status=status.HTTP_201_CREATED, safe=False)
            response['Location'] = 'http://127.0.0.1:8100/api/v1/orders/{user_uid}/purchase/{order_uid}'.format(
                user_uid=user_uid, order_uid=orderResp["orderUid"])
            return response
        JsonResponse({'message': 'Item not available'}, status=status.HTTP_409_CONFLICT)
    return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def get_order_warranty(request, user_uid, order_uid):
    if validUser(user_uid):
        storeReq = requests.post('http://127.0.0.1:8100/api/v1/orders/{}/warranty'.format(order_uid), json=request.data).json()
        storeReq.update({'orderUid': order_uid})
        return JsonResponse(storeReq, status=status.HTTP_200_OK)
    return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def get_order_refund(request, user_uid, order_uid):
    if validUser(user_uid):
        storeReq = requests.delete('http://127.0.0.1:8100/api/v1/orders/{}'.format(order_uid))
        if storeReq.status_code == 404:
            storeReq = storeReq.json()
            return JsonResponse(storeReq, status=status.HTTP_404_NOT_FOUND, safe=False)
        return JsonResponse(1, status=status.HTTP_204_NO_CONTENT, safe=False)
    return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)


# Support function
def filter_response(storeReq):
    if type(storeReq) is dict:
        storeReq['date'] = storeReq['orderDate']
        storeReq['warrantyStatus'] = storeReq['status']
        del storeReq['itemUid'], storeReq['status'], storeReq['orderDate'], storeReq['id'], storeReq['available_count']
    else:
        for item in storeReq:
            if 'date' and 'warrantyStatus' and 'itemUid' in item:
                item['date'] = item['orderDate']
                item['warrantyStatus'] = item['status']
                del item['itemUid'], item['status'], item['orderDate']
            if 'id' in item:
                del item['id']
            if 'available_count' in item:
                del item['available_count']
    return storeReq


def validUser(user_uid):
    try:
        return Store.objects.get(user_uid=user_uid)
    except ValidationError:
        return False
