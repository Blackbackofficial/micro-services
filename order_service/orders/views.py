from circuitbreaker import circuit
from rest_framework.parsers import JSONParser
from .functions import FunctionsOrders
from .models import Orders
from .serializers import OrdersSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
import requests

FAILURES = 3
TIMEOUT = 6


# API
@circuit(failure_threshold=FAILURES, recovery_timeout=TIMEOUT)
@api_view(['GET', 'POST', 'DELETE'])
def actions_orders(request, user_uid):
    """
    GET /api/v1/orders/{userUid} – get all user orders.
    POST /api/v1/orders/{userUid} – place an order on behalf of the user.
    DELETE /api/v1/orders/{orderUid} – return order.
    :param request: request for data in JSON
    :param user_uid: User Uid
    :return: 1) Get all user's orders 2) Create and return order_uid 3) Delete order and close warranty
    """

    try:
        if request.method == 'GET':
            orders = Orders.objects.all().filter(user_uid=user_uid)
            filterReq = FunctionsOrders.filter_response(orders)
            return JsonResponse(filterReq, status=status.HTTP_200_OK, safe=False)

        if not FunctionsOrders.pingServices(1):
            return JsonResponse({'message': 'Server Warranty/Warehouse close'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'POST':
            parseDict = JSONParser().parse(request)
            if FunctionsOrders.regularExp(parseDict, 1) is False:
                return JsonResponse({'message': 'Error validation reason'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            order = dict(status='PAID', user_uid=user_uid)
            order_serializer = OrdersSerializer(data=order)

            if order_serializer.is_valid():
                order_serializer.save()
            parseDict.update(
                {'orderUid': order_serializer.data["order_uid"], 'orderItemUid': order_serializer.data["item_uid"]})
            warrantyResp = requests.post(
                'https://warranty-ivan.herokuapp.com/api/v1/warranty/{}'.format(order_serializer.data["item_uid"]))
            warehouseResp = requests.post('https://warehouse-ivan.herokuapp.com/api/v1/warehouse/', json=parseDict)
            # rolling back the operation
            if warrantyResp.status_code == 204 and warehouseResp.status_code == 200:
                return JsonResponse({"orderUid": order_serializer.data["order_uid"]}, status=status.HTTP_200_OK)
            else:
                initOrder = Orders.objects.get(order_uid=parseDict['orderUid'])
                requests.delete('https://orders-ivan.herokuapp.com/api/v1/orders/{}'.format(parseDict['orderUid']))
                requests.delete('https://warranty-ivan.herokuapp.com/api/v1/warranty/{}'.format(initOrder))
                requests.delete('https://warehouse-ivan.herokuapp.com/api/v1/warehouse/{}'.format(initOrder))
                return JsonResponse({'message': 'Rolling back operation'}, status=status.HTTP_409_CONFLICT)

        if request.method == 'DELETE':
            try:
                initOrder = order = Orders.objects.get(order_uid=user_uid)
                initOrder = initOrder.item_uid
                warehouseResp = requests.delete(
                    'https://warehouse-ivan.herokuapp.com/api/v1/warehouse/{}'.format(initOrder))
                warrantyResp = requests.delete(
                    'https://warranty-ivan.herokuapp.com/api/v1/warranty/{}'.format(initOrder))
                if warehouseResp.status_code and warrantyResp.status_code == 204:
                    order.delete()
                    return JsonResponse(1, status=status.HTTP_204_NO_CONTENT, safe=False)
                return JsonResponse({'message': 'Warranty or Warehouse {} not found'.format(user_uid)},
                                    status=status.HTTP_404_NOT_FOUND)
            except Orders.DoesNotExist:
                return JsonResponse({'message': 'Order {} not found'.format(user_uid)},
                                    status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


@circuit(failure_threshold=FAILURES, recovery_timeout=TIMEOUT)
@api_view(['GET'])
def one_order(request, user_uid, order_uid):
    """
    GET /api/v1/orders/{userUid}/{orderUid} – get information on a specific user order
    :param request: none used
    :param user_uid: User Uid
    :param order_uid: Order Uid
    :return: return one user's order (user_uid, order_uid)
    """

    try:
        orders = Orders.objects.all().filter(user_uid=user_uid, order_uid=order_uid)
        if orders.exists():
            filterReq = FunctionsOrders.filter_response(orders)
            return JsonResponse(filterReq[0], status=status.HTTP_200_OK, safe=False)
        return JsonResponse({'message': 'Not found order {order_uid} for user {user_uid}'.format(
            order_uid=order_uid, user_uid=user_uid)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


@circuit(failure_threshold=FAILURES, recovery_timeout=TIMEOUT)
@api_view(['POST'])
def warranty_order(request, order_uid):
    """
    POST /api/v1/orders/{orderUid}/warranty – order guarantee request;
    :param request: request for data in JSON
    :param order_uid: Order Uid
    :return: warranty's data
    """

    try:
        parseDict = JSONParser().parse(request)
        if FunctionsOrders.regularExp(parseDict, 2) is False:
            return JsonResponse({'message': 'Error validation reason'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not FunctionsOrders.pingServices(2):
            return JsonResponse({'message': 'Service Warehouse close'}, status=status.HTTP_410_GONE)

        item_uid = Orders.objects.get(order_uid=order_uid).item_uid
        warehouseResp = requests.post('https://warehouse-ivan.herokuapp.com/api/v1/warehouse/{}/warranty'
                                      .format(item_uid), json=parseDict)

        if warehouseResp.status_code == 200:
            return JsonResponse(warehouseResp.json(), status=status.HTTP_200_OK)
        return JsonResponse({'message': 'Not found order {}'.format(order_uid)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)
