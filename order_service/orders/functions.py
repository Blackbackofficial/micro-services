from urllib.error import HTTPError
from .serializers import OrdersSerializer
from django.http import JsonResponse
from rest_framework import status
from urllib.request import urlopen
import re


class FunctionsOrders:
    """
    Support function for orders service
    """

    def pingServices(self):
        """
        Checking the health of other services.
        :return: True or False
        """

        try:
            if self == 1:
                urlopen("https://warranty-ivan.herokuapp.com/manage/health/")
                urlopen("https://warehouse-ivan.herokuapp.com/manage/health/")
            elif self == 2:
                urlopen("https://warehouse-ivan.herokuapp.com/manage/health/")
            return True
        except HTTPError:
            return False

    def filter_response(self):
        """
        Sorts the response, removes unnecessary data.
        :param self: dict all user orders
        :return: reformed storeReq
        """

        try:
            orders_serializer = OrdersSerializer(self, many=True).data
            for item in orders_serializer:
                item['orderUid'] = item['order_uid']
                item['itemUid'] = item['item_uid']
                item['orderDate'] = item['order_date']
                del item['order_uid'], item['item_uid'], item['order_date'], item['id'], item['user_uid']
            return orders_serializer
        except Exception as e:
            return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)

    def regularExp(self, types):
        """
        Validation of data from JSON(request) using a pattern from regular expressions
        :param self: from function in JSON(request)
        :param types: types of check for regular expressions
        :return: True or False
        """

        model = '^[A-Z]+[a-z 0-9]+$'
        size = '^[A-Z]+$'
        reason = '^[A-Z][a-z 0-9]+$'
        if types == 1 and (re.match(model, self.get("model")) and re.match(size, self.get("size"))) is not None:
            return True
        if types == 2 and re.match(reason, self.get("reason")) is not None:
            return True
        return False

