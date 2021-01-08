from urllib.error import HTTPError
from uuid import UUID

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Store
from urllib.request import urlopen
import requests
import re


# API
@api_view(['GET'])
def get_orders(request, user_uid):
    try:
        if not pingServices():
            return JsonResponse({'message': 'Server Orders/Warranty/Warehouse close'}, status=status.HTTP_404_NOT_FOUND)
        elif validate_uuid4(user_uid) is False:
            return JsonResponse({'message': 'Is not a valid UUID'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif validUser(user_uid):
            storeReq = requests.get('https://orders-ivan.herokuapp.com/api/v1/orders/{}'.format(user_uid)).json()
            for item in storeReq:
                warrantyResp = requests.get(
                    'https://warranty-ivan.herokuapp.com/api/v1/warranty/{}'.format(item['itemUid'])).json()
                warehouseResp = requests.get(
                    'https://warehouse-ivan.herokuapp.com/api/v1/warehouse/{}'.format(item['itemUid'])).json()
                item.update(warrantyResp, **warehouseResp)
            storeReq = filter_response(storeReq)
            return JsonResponse(storeReq, status=status.HTTP_200_OK, safe=False)
        return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_order(request, user_uid, order_uid):
    try:
        if not pingServices():
            return JsonResponse({'message': 'Server Orders/Warranty/Warehouse close'}, status=status.HTTP_404_NOT_FOUND)
        elif (validate_uuid4(user_uid) and validate_uuid4(order_uid)) is False:
            return JsonResponse({'message': 'Is not a valid UUID'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif validUser(user_uid):
            storeReq = requests.get('https://orders-ivan.herokuapp.com/api/v1/orders/{user_uid}/{order_uid}'.format(
                user_uid=user_uid, order_uid=order_uid)).json()
            if 'message' in storeReq:
                return JsonResponse({'message': '{}'.format(storeReq.get('message'))},
                                    status=status.HTTP_400_BAD_REQUEST)
            warrantyResp = requests.get(
                'https://warranty-ivan.herokuapp.com/api/v1/warranty/{}'.format(storeReq['itemUid'])).json()
            warehouseResp = requests.get(
                'https://warehouse-ivan.herokuapp.com/api/v1/warehouse/{}'.format(storeReq['itemUid'])).json()
            storeReq.update(warrantyResp, **warehouseResp)  # через дополнительные параметры конструктора типа
            storeReq = filter_response(storeReq)
            return JsonResponse(storeReq, status=status.HTTP_200_OK)
        return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def purchase_order(request, user_uid):
    try:
        if not pingServices():
            return JsonResponse({'message': 'Server Orders/Warranty/Warehouse close'}, status=status.HTTP_404_NOT_FOUND)
        elif validate_uuid4(user_uid) is False:
            return JsonResponse({'message': 'Is not a valid UUID'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif validUser(user_uid):
            if len(request.data) <= 2 and ('model' and 'size') in request.data:
                if regularExp(request.data) is False:
                    return JsonResponse({'message': 'Error validation model or size'},
                                        status=status.HTTP_406_NOT_ACCEPTABLE)
                # надо подумать
                orderResp = requests.post('https://orders-ivan.herokuapp.com/api/v1/orders/{}'
                                          .format(user_uid), json=request.data)
                if orderResp.status_code == 200:
                    orderResp = orderResp.json()
                    response = JsonResponse(1, status=status.HTTP_201_CREATED, safe=False)
                    response['Location'] = 'https://orders-ivan.herokuapp.com/api/v1/orders/{user_uid}/purchase/' \
                                           '{order_uid}'.format(user_uid=user_uid, order_uid=orderResp["orderUid"])
                    return response
                JsonResponse({'message': 'Item not available'}, status=status.HTTP_409_CONFLICT)
            else:
                return JsonResponse({'message': 'Incorrect JSON format or model, size'},
                                    status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_order_warranty(request, user_uid, order_uid):
    try:
        if not pingServices():
            return JsonResponse({'message': 'Server Orders/Warranty/Warehouse close'}, status=status.HTTP_404_NOT_FOUND)
        elif (validate_uuid4(user_uid) and validate_uuid4(order_uid)) is False:
            return JsonResponse({'message': 'Is not a valid UUID'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif validUser(user_uid):
            storeReq = requests.post('https://orders-ivan.herokuapp.com/api/v1/orders/{}/warranty'.format(order_uid),
                                     json=request.data).json()
            storeReq.update({'orderUid': order_uid})
            return JsonResponse(storeReq, status=status.HTTP_200_OK)
        return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def get_order_refund(request, user_uid, order_uid):
    try:
        if not pingServices():
            return JsonResponse({'message': 'Server Orders/Warranty/Warehouse close'}, status=status.HTTP_404_NOT_FOUND)
        elif (validate_uuid4(user_uid) and validate_uuid4(order_uid)) is False:
            return JsonResponse({'message': 'Is not a valid UUID'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif validUser(user_uid):
            storeReq = requests.delete('https://orders-ivan.herokuapp.com/api/v1/orders/{}'.format(order_uid))
            if storeReq.status_code == 404:
                storeReq = storeReq.json()
                return JsonResponse(storeReq, status=status.HTTP_404_NOT_FOUND, safe=False)
            return JsonResponse(1, status=status.HTTP_204_NO_CONTENT, safe=False)
        return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


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


def regularExp(request):
    model = '^[A-Z]+[a-z 0-9]+$'
    size = '^[A-Z]+$'
    if (re.match(model, request.get("model")) and re.match(size, request.get("size"))) is not None:
        return True
    return False


def pingServices():
    try:
        urlopen("https://warranty-ivan.herokuapp.com/manage/health/")
        urlopen("https://warehouse-ivan.herokuapp.com/manage/health/")
        urlopen('https://orders-ivan.herokuapp.com/manage/health/')
        return True
    except HTTPError:
        return False


def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
    except ValueError:
        return False
    return True
