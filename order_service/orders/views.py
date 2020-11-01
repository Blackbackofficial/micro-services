from rest_framework.parsers import JSONParser
from .models import Orders
from .serializers import OrdersSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def make_orders(request, user_uid):
    if request.method == 'POST':
        store_data = JSONParser().parse(request)
        order = dict(status='PAID', user_uid=user_uid)
        order_serializer = OrdersSerializer(data=order)
        if order_serializer.is_valid():
            order_serializer.save()
            # Логика
            return JsonResponse({"orderUid": order_serializer.data["order_uid"]}, status=status.HTTP_200_OK)
    if request.method == 'GET':
        orders = Orders.objects.all().filter(user_uid=user_uid)
        filter_req = filter_response(orders)
        return JsonResponse(filter_req, status=status.HTTP_200_OK, safe=False)
    if request.method == 'DELETE':
        try:
            order_safe = Orders.objects.get(order_uid=user_uid)
            order_safe.delete()
            return JsonResponse(1, status=status.HTTP_204_NO_CONTENT, safe=False)
        except Orders.DoesNotExist:
            return JsonResponse({'message': 'Order {} not found'.format(user_uid)}, status=status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse('', status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def one_order(request, user_uid, order_uid):
    orders = Orders.objects.all().filter(user_uid=user_uid, order_uid=order_uid)
    if orders.exists():
        filter_req = filter_response(orders)
        return JsonResponse(filter_req[0], status=status.HTTP_200_OK, safe=False)
    return JsonResponse({'message': 'Not found order {order_uid} for user {user_uid}'.format(
        order_uid=order_uid, user_uid=user_uid)}, status=status.HTTP_404_NOT_FOUND)


def filter_response(orders):
    orders_serializer = OrdersSerializer(orders, many=True)
    for item in orders_serializer.data:
        item['orderUid'] = item['order_uid']
        item['itemUid'] = item['item_uid']
        item['orderDate'] = item['order_date']
        del item['order_uid'], item['item_uid'], item['order_date']
    return orders_serializer.data
