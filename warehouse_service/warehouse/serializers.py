from rest_framework_json_api import serializers
from .models import Items, Order_item


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Items
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order_item
        fields = '__all__'
