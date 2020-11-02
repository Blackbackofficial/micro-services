from rest_framework_json_api import serializers
from .models import Warranty


class WarrantySerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    class Meta:
        model = Warranty
        fields = '__all__'
