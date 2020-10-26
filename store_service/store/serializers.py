from rest_framework import serializers
from store.models import Store


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'name', 'user_uid')
