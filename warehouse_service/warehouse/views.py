from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .functions import FunctionsWarehouse
from .models import Items, Order_item
from .serializers import ItemSerializer, OrderItemSerializer
from django.http import JsonResponse
from rest_framework import status
import requests


# API
@api_view(['POST'])
def post_items(request):
    """
    POST /api/v1/warehouse – request to receive items from the warehouse for a new order.
    :param request: request for data's JSON
    :return: orderUid, model, size
    """

    try:
        if len(request.data) <= 4 and ('model' and 'size' and 'orderUid') in request.data:
            parseDict = request.data
            if FunctionsWarehouse.regularExp(parseDict, 1) is False:
                return JsonResponse({'message': 'Error validation model/size'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if FunctionsWarehouse.validate_uuid4(parseDict['orderUid']) is False:
                return JsonResponse({'message': 'Is not a valid UUID'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return JsonResponse({'message': 'Incorrect JSON format/model/size'}, status=status.HTTP_400_BAD_REQUEST)

        instData = instItem = Items.objects.get(model=parseDict['model'])
        instData = ItemSerializer(instData).data
        if instData['available_count'] == 0:
            return JsonResponse({'message': 'Item not available'}, status=status.HTTP_409_CONFLICT)

        instData['available_count'] -= 1
        req_serializer = ItemSerializer(instance=instItem, data=instData)

        if req_serializer.is_valid():
            req_serializer.save()
        orderItem = dict(order_uid=parseDict['orderUid'], item_id=instData['id'])

        if 'orderItemUid' in parseDict:
            orderItem.update({'order_item_uid': parseDict['orderItemUid']})
        item_serializer = OrderItemSerializer(data=orderItem)

        if item_serializer.is_valid():
            item_serializer.save()
        order = Order_item.objects.get(order_uid=parseDict['orderUid']).order_item_uid
        req = dict(orderItemUid=order, orderUid=parseDict['orderUid'], model=parseDict['model'], size=parseDict['size'])
        return JsonResponse(req, status=status.HTTP_200_OK)
    except Items.DoesNotExist:
        return JsonResponse({'message': 'Requested \'{}\' not find'.format(parseDict['orderUid'])},
                            status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def request_warranty(request, orderItemUid):
    """
    POST /api/v1/warehouse/{itemUid}/warranty – warranty solution request;
    :param request: JSON hidden in the data in request
    :param orderItemUid: order's item Uid
    :return: requests from Warranty
    """

    try:
        parseDict = JSONParser().parse(request)
        if FunctionsWarehouse.regularExp(parseDict, 2) is False:
            return JsonResponse({'message': 'Error validation reason'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        orderItem = Order_item.objects.get(order_item_uid=orderItemUid).item_id
        availableCount = Items.objects.get(id=orderItem).available_count
        resJson = dict(availableCount=availableCount, reason=parseDict['reason'])
        requestW = requests.post('https://warranty-ivan.herokuapp.com/api/v1/warranty/{}/warranty'.format(orderItemUid),
                                 json=resJson)
        if requestW.status_code == 404:
            return JsonResponse({'message': 'Warranty not found for itemUid \'{}\''.format(orderItemUid)},
                                status=status.HTTP_404_NOT_FOUND)
        return JsonResponse(requestW.json(), status=status.HTTP_200_OK)
    except Order_item.DoesNotExist:
        return JsonResponse({'message': 'Order \'{}\' not find'.format(orderItemUid)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def request_items(request, orderItemUid):
    """
    GET /api/v1/warehouse/{itemUid} – information about things in stock.
    DELETE /api/v1/warehouse/{itemUid} - return the order to the warehouse.
    :param request: request to determine GET or DELETE
    :param orderItemUid: order's item Uid to determine order on 'orderItemUid'
    :return: 1) GET all items 2) DELETE the order is returned and 1 is added
    """

    try:
        instOrder = orderItem = Order_item.objects.get(order_item_uid=orderItemUid)
        instData = items = Items.objects.get(id=orderItem.item_id)
        items = ItemSerializer(items).data
    except Order_item.DoesNotExist:
        return JsonResponse({'message': 'Order \'{}\' not find'.format(orderItemUid)}, status=status.HTTP_404_NOT_FOUND)

    try:
        if request.method == 'GET':
            return JsonResponse(items, status=status.HTTP_200_OK, safe=False)

        if request.method == 'DELETE':
            items['available_count'] += 1
            data_serializer = ItemSerializer(instance=instData, data=items)

            if data_serializer.is_valid():
                data_serializer.save()
            orderItem = OrderItemSerializer(orderItem).data
            orderItem['canceled'] = True
            order_serializer = OrderItemSerializer(instance=instOrder, data=orderItem)

            if order_serializer.is_valid():
                order_serializer.save()
                return JsonResponse(1, status=status.HTTP_204_NO_CONTENT, safe=False)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)
