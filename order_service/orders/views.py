from rest_framework.parsers import JSONParser
from .models import Orders
from .serializers import OrdersSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from urllib.request import urlopen
import requests
import re


@api_view(['GET', 'POST', 'DELETE'])
def actions_orders(request, user_uid):
    try:
        if request.method == 'GET':
            orders = Orders.objects.all().filter(user_uid=user_uid)
            filterReq = filter_response(orders)
            return JsonResponse(filterReq, status=status.HTTP_200_OK, safe=False)

        # ping on warranty and warehouse service
        urlopen("https://warranty-ivan.herokuapp.com/manage/health/")
        urlopen("https://warehouse-ivan.herokuapp.com/manage/health/")

        if request.method == 'POST':
            parseDict = JSONParser().parse(request)
            if regularExp(parseDict, 1) is False:
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
            if warrantyResp.status_code == 204 and warehouseResp.status_code == 200:
                return JsonResponse({"orderUid": order_serializer.data["order_uid"]}, status=status.HTTP_200_OK)
            return JsonResponse({"message": "Error on warranty or warehouse service"}, status=status.HTTP_200_OK)

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


@api_view(['GET'])
def one_order(request, user_uid, order_uid):
    try:
        orders = Orders.objects.all().filter(user_uid=user_uid, order_uid=order_uid)
        if orders.exists():
            filterReq = filter_response(orders)
            return JsonResponse(filterReq[0], status=status.HTTP_200_OK, safe=False)
        return JsonResponse({'message': 'Not found order {order_uid} for user {user_uid}'.format(
            order_uid=order_uid, user_uid=user_uid)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def warranty_order(request, order_uid):
    try:
        parseDict = JSONParser().parse(request)
        if regularExp(parseDict, 2) is False:
            return JsonResponse({'message': 'Error validation reason'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        item_uid = Orders.objects.get(order_uid=order_uid).item_uid
        warehouseResp = requests.post('https://warehouse-ivan.herokuapp.com/api/v1/warehouse/{}/warranty'
                                      .format(item_uid), json=parseDict)
        if warehouseResp.status_code == 200:
            return JsonResponse(warehouseResp.json(), status=status.HTTP_200_OK)
        return JsonResponse({'message': 'Not found order {}'.format(order_uid)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


# Support function
def filter_response(orders):
    try:
        orders_serializer = OrdersSerializer(orders, many=True).data
        for item in orders_serializer:
            item['orderUid'] = item['order_uid']
            item['itemUid'] = item['item_uid']
            item['orderDate'] = item['order_date']
            del item['order_uid'], item['item_uid'], item['order_date'], item['id'], item['user_uid']
        return orders_serializer
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


def regularExp(request, types):
    model = '^[A-Z]+[a-z 0-9]+$'
    size = '^[A-Z]+$'
    reason = '^[A-Z][a-z 0-9]+$'
    if types == 1 and (re.match(model, request.get("model")) and re.match(size, request.get("size"))) is not None:
        return True
    if types == 2 and re.match(reason, request.get("reason")) is not None:
        return True
    return False
