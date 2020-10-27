from rest_framework import serializers
from orders.models import Orders


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ('id', 'item_uid', 'order_date', 'order_uid', 'status', 'user_uid')
