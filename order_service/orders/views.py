from .serializers import OrdersSerializer
from django.http import JsonResponse
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.db import connection
from datetime import datetime, timezone


@api_view(['POST'])
def make_orders(request, user_uid):
    if request.method == 'POST':
        # store_data = JSONParser().parse(request)
        order = dict(status='PAID', user_uid=user_uid)
        order_serializer = OrdersSerializer(data=order)
        if order_serializer.is_valid():
            order_serializer.save()
            # Логика
            return JsonResponse({"orderUid": order_serializer.data["order_uid"]}, status=status.HTTP_200_OK)
    else:
        return JsonResponse('', status=status.HTTP_405_METHOD_NOT_ALLOWED)


class HealthCheckCustom(View):
    def get(self, *args, **kwargs):
        utc_time = datetime.now(timezone.utc)
        local_time = utc_time.astimezone()
        offset = local_time.utcoffset().total_seconds()
        if offset == 0.0:
            offset = "None"

        db_name = connection.settings_dict['NAME']

        with connection.cursor() as cursor:
            cursor.execute("select 1")
            one = cursor.fetchone()[0]
            if one != 1:
                raise Exception('The site did not pass the health check')
            return JsonResponse({"status": "Work",
                                 "components": {
                                     "db": {
                                         "status": "Work",
                                         "name": db_name,
                                         "database": "PostgreSQL"
                                     },
                                     "ping": {
                                         "status": "Work"
                                     },
                                     "time": {
                                         "epoch": int(utc_time.timestamp()),
                                         "local": local_time.isoformat(),
                                         "offset": offset
                                     }
                                 }}, status=status.HTTP_200_OK)

