from rest_framework.parsers import JSONParser

from .serializers import OrdersSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['POST'])
def make_orders(request, user_uid):
    if request.method == 'POST':
        store_data = JSONParser().parse(request)
        order = dict(status='PAID', user_uid=user_uid)
        order_serializer = OrdersSerializer(data=order)
        if order_serializer.is_valid():
            order_serializer.save()
            # Логика
            return JsonResponse({"orderUid": order_serializer.data["order_uid"]}, status=status.HTTP_200_OK)
    else:
        return JsonResponse('', status=status.HTTP_405_METHOD_NOT_ALLOWED)
