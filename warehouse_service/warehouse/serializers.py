from rest_framework_json_api import serializers
from .models import Items, Order_item


class ItemSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.available_count = validated_data.get('available_count', instance.available_count)
        instance.save()
        return instance

    class Meta:
        model = Items
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.canceled = validated_data.get('canceled', instance.canceled)
        instance.save()
        return instance

    class Meta:
        model = Order_item
        fields = '__all__'
