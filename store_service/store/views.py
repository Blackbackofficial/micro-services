from circuitbreaker import circuit
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from .functions import FunctionsStore
import requests

FAILURES = 3
TIMEOUT = 6


# API
@circuit(failure_threshold=FAILURES, recovery_timeout=TIMEOUT)
@api_view(['GET'])
def get_orders(request, user_uid):
    """
    GET /api/v1/store/{userUid}/orders - get a list of user's orders + add degradation of functionality services
    :param request: none used
    :param user_uid: User Uid
    :return: storeReq (data)
    """

    try:
        if not FunctionsStore.pingDegradation('https://orders-ivan.herokuapp.com/manage/health/'):
            return JsonResponse({'message': 'Server Orders close'}, status=status.HTTP_404_NOT_FOUND)

        if FunctionsStore.validate_uuid4(user_uid) is False:
            return JsonResponse({'message': 'Is not a valid UUID'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        # ping to degradation of functionality services
        pingWarranty = FunctionsStore.pingDegradation("https://warranty-ivan.herokuapp.com/manage/health/")
        pingWarehouse = FunctionsStore.pingDegradation("https://warehouse-ivan.herokuapp.com/manage/health/")

        if not FunctionsStore.validUser(user_uid):
            return JsonResponse({'message': 'The user does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)

        storeReq = requests.get('https://orders-ivan.herokuapp.com/api/v1/orders/{}'.format(user_uid)).json()
        warrantyResp = warehouseResp = {}
        for item in storeReq:
            if pingWarranty:
                warrantyResp = requests.get(
                    'https://warranty-ivan.herokuapp.com/api/v1/warranty/{}'.format(item['itemUid'])).json()
            if pingWarehouse:
                warehouseResp = requests.get(
                    'https://warehouse-ivan.herokuapp.com/api/v1/warehouse/{}'.format(item['itemUid'])).json()
            item.update(warrantyResp, **warehouseResp)  # через дополнительные параметры конструктора типа

        storeReq = FunctionsStore.filter_response(storeReq)
        return JsonResponse(storeReq, status=status.HTTP_200_OK, safe=False)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


@circuit(failure_threshold=FAILURES, recovery_timeout=TIMEOUT)
@api_view(['GET'])
def get_order(request, user_uid, order_uid):
    """
    GET /api/v1/store/{userUid}/{orderUid} – information on a specific(user_uid, order_uid) order.
    :param request: none used
    :param user_uid: User Uid
    :param order_uid: Order Uid
    :return: storeReq (data)
    """

    try:
        if not FunctionsStore.pingDegradation('https://orders-ivan.herokuapp.com/manage/health/'):
            return JsonResponse({'message': 'Server Orders close'}, status=status.HTTP_404_NOT_FOUND)

        if (FunctionsStore.validate_uuid4(user_uid) and FunctionsStore.validate_uuid4(order_uid)) is False:
            return JsonResponse({'message': 'Is not a valid UUID'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not FunctionsStore.validUser(user_uid):
            return JsonResponse({'message': 'The user does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)

        # ping to degradation of functionality services
        pingWarranty = FunctionsStore.pingDegradation("https://warranty-ivan.herokuapp.com/manage/health/")
        pingWarehouse = FunctionsStore.pingDegradation("https://warehouse-ivan.herokuapp.com/manage/health/")
        storeReq = requests.get('https://orders-ivan.herokuapp.com/api/v1/orders/{user_uid}/{order_uid}'.format(
            user_uid=user_uid, order_uid=order_uid)).json()
        warrantyResp = warehouseResp = {}
        if pingWarranty:
            warrantyResp = requests.get(
                'https://warranty-ivan.herokuapp.com/api/v1/warranty/{}'.format(storeReq['itemUid'])).json()
        if pingWarehouse:
            warehouseResp = requests.get(
                'https://warehouse-ivan.herokuapp.com/api/v1/warehouse/{}'.format(storeReq['itemUid'])).json()
        storeReq.update(warrantyResp, **warehouseResp)  # через дополнительные параметры конструктора типа
        storeReq = FunctionsStore.filter_response(storeReq)
        return JsonResponse(storeReq, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


@circuit(failure_threshold=FAILURES, recovery_timeout=TIMEOUT)
@api_view(['POST'])
def purchase_order(request, user_uid):
    """
    POST /api/v1/store/{userUid}/purchase – complete purchase
    :param request: JSON hidden in the data
    :param user_uid: User Uid
    :return: in Header ['Location'] + Susses(1, status 201) or not
    """

    try:
        if not FunctionsStore.pingServices():
            return JsonResponse({'message': 'Server Orders/Warranty/Warehouse close'}, status=status.HTTP_404_NOT_FOUND)

        if FunctionsStore.validate_uuid4(user_uid) is False:
            return JsonResponse({'message': 'Is not a valid UUID'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not FunctionsStore.validUser(user_uid):
            return JsonResponse({'message': 'The user does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)

        if len(request.data) <= 2 and ('model' and 'size') in request.data:
            if FunctionsStore.regularExp(request.data) is False:
                return JsonResponse({'message': 'No valid model or size'}, status=status.HTTP_406_NOT_ACCEPTABLE)
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
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


@circuit(failure_threshold=FAILURES, recovery_timeout=TIMEOUT)
@api_view(['POST'])
def get_order_warranty(request, user_uid, order_uid):
    """
    POST /api/v1/store/{userUid}/{orderUid}/warranty – order warranty request;
    :param request: used to send data to the warranty service
    :param user_uid: User Uid
    :param order_uid: Order Uid
    :return: storeReq (data with warranty, status 200)
    """

    try:
        if not FunctionsStore.pingServices():
            return JsonResponse({'message': 'Server Orders/Warranty/Warehouse close'}, status=status.HTTP_404_NOT_FOUND)

        elif (FunctionsStore.validate_uuid4(user_uid) and FunctionsStore.validate_uuid4(order_uid)) is False:
            return JsonResponse({'message': 'Is not a valid UUID'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        elif FunctionsStore.validUser(user_uid):
            storeReq = requests.post('https://orders-ivan.herokuapp.com/api/v1/orders/{}/warranty'.format(order_uid),
                                     json=request.data).json()
            storeReq.update({'orderUid': order_uid})
            return JsonResponse(storeReq, status=status.HTTP_200_OK)
        return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


@circuit(failure_threshold=FAILURES, recovery_timeout=TIMEOUT)
@api_view(['DELETE'])
def get_order_refund(request, user_uid, order_uid):
    """
    DELETE /api/v1/store/{userUid}/{orderUid}/refund – return order;
    :param request: none used
    :param user_uid: User Uid
    :param order_uid: Order Uid
    :return: Susses(1, status 201) or not
    """

    try:
        if not FunctionsStore.pingServices():
            return JsonResponse({'message': 'Server Orders/Warranty/Warehouse close'}, status=status.HTTP_404_NOT_FOUND)

        elif (FunctionsStore.validate_uuid4(user_uid) and FunctionsStore.validate_uuid4(order_uid)) is False:
            return JsonResponse({'message': 'Is not a valid UUID'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        elif FunctionsStore.validUser(user_uid):
            storeReq = requests.delete('https://orders-ivan.herokuapp.com/api/v1/orders/{}'.format(order_uid))
            if storeReq.status_code == 404:
                storeReq = storeReq.json()
                return JsonResponse(storeReq, status=status.HTTP_404_NOT_FOUND, safe=False)
            return JsonResponse(1, status=status.HTTP_204_NO_CONTENT, safe=False)
        return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)
