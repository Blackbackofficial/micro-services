from rest_framework import serializers
from .models import Orders


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ('item_uid', 'order_date', 'order_uid', 'status')
