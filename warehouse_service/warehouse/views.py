from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .models import Items, Order_item
from .serializers import ItemSerializer, OrderItemSerializer
from django.http import JsonResponse
from rest_framework import status
import requests


# API
@api_view(['POST'])
def post_items(request):
    parseDict = JSONParser().parse(request)
    try:
        req_data = req_items = Items.objects.get(model=parseDict['model'])
        req_data = ItemSerializer(req_data).data
        req_data['available_count'] -= 1
        if req_data['available_count'] == 0:
            return JsonResponse({'message': 'Item not available'}, status=status.HTTP_409_CONFLICT)
        req_serializer = ItemSerializer(instance=req_items, data=req_data)
        if req_serializer.is_valid():
            req_serializer.save()
        order_item = dict(order_uid=parseDict['orderUid'], item_id=req_data['id'])
        item_serializer = OrderItemSerializer(data=order_item)
        if item_serializer.is_valid():
            item_serializer.save()
        order = Order_item.objects.get(order_uid=parseDict['orderUid']).order_item_uid
        req = dict(orderItemUid=order, orderUid=parseDict['orderUid'], model=parseDict['model'], size=parseDict['size'])
        return JsonResponse(req, status=status.HTTP_200_OK)
    except Items.DoesNotExist:
        return JsonResponse({'message': 'Requested item not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'DELETE'])
def request_items(request, orderItemUid):
    try:
        startOrder = order = Order_item.objects.get(order_item_uid=orderItemUid)
        startData = req_data = Items.objects.get(id=order.item_id)
        req_data = ItemSerializer(req_data).data
    except Order_item.DoesNotExist:
        return JsonResponse({'message': 'Order item not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        del req_data['id'], req_data['available_count']
        return JsonResponse(req_data, status=status.HTTP_200_OK, safe=False)
    if request.method == 'DELETE':
        req_data['available_count'] += 1
        req_serializer = ItemSerializer(instance=startData, data=req_data)
        if req_serializer.is_valid():
            req_serializer.save()
        order = OrderItemSerializer(order).data
        order['canceled'] = True
        order_serializer = OrderItemSerializer(instance=startOrder, data=order)
        if order_serializer.is_valid():
            order_serializer.save()
        return JsonResponse(1, status=status.HTTP_204_NO_CONTENT, safe=False)


@api_view(['POST'])
def request_warranty(request, orderItemUid):
    parseDict = JSONParser().parse(request)
    try:
        item_id = Order_item.objects.get(order_item_uid=orderItemUid).item_id
        available_count = Items.objects.get(id=item_id).available_count
        resJson = dict(available_count=available_count, reason=parseDict['reason'])
        warranty_req = requests.post('http://127.0.0.1:8200/api/v1/warranty/{}/warranty'.format(orderItemUid), json=resJson)
        if warranty_req.status_code == 404:
            return JsonResponse({'message': 'Warranty not found for itemUid \'{}\''.format(orderItemUid)}, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse(warranty_req.json(), status=status.HTTP_200_OK)
    except Order_item.DoesNotExist:
        return JsonResponse({'message': 'Order item not found'}, status=status.HTTP_404_NOT_FOUND)
