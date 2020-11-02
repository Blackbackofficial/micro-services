from rest_framework.parsers import JSONParser
from .models import Warranty
from .serializers import WarrantySerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view


# API
@api_view(['GET', 'POST', 'DELETE'])
def actions_warranty(request, item_uid):
    if request.method == 'POST':
        warranty = dict(status='ON_WARRANTY', item_uid=item_uid, comment='None')
        warranty_serializer = WarrantySerializer(data=warranty)
        if warranty_serializer.is_valid():
            warranty_serializer.save()
            return JsonResponse(1, status=status.HTTP_204_NO_CONTENT, safe=False)
    if request.method == 'GET':
        if validWarranty(item_uid):
            warranty = validWarranty(item_uid)
            filter_res = filter_response(warranty)
            return JsonResponse(filter_res, status=status.HTTP_200_OK, safe=False)
        return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        if validWarranty(item_uid):
            warranty_delete = validWarranty(item_uid)
            warranty_delete.delete()
            return JsonResponse(1, status=status.HTTP_204_NO_CONTENT, safe=False)
        return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def request_warranty(request, item_uid):
    if validWarranty(item_uid):
        warranty_update = warranty_data = validWarranty(item_uid)
        warranty_data = WarrantySerializer(warranty_data)
        security_post = JSONParser().parse(request)
        decision = dict(warrantyDate=warranty_data.data['warranty_date'])
        if warranty_data.data['status'] == 'ON_WARRANTY':
            warranty_data = warranty_data.data
            warranty_data['status'] = 'USE_WARRANTY'
            warranty_data = WarrantySerializer(instance=warranty_update, data=warranty_data)
            if warranty_data.is_valid():
                warranty_data.save()
            if security_post['availableCount'] > 1:
                decision['decision'] = 'RETURN'
            else:
                decision['decision'] = 'FIXING'
        else:
            decision['decision'] = 'REFUSED'
        return JsonResponse(decision, status=status.HTTP_200_OK)
    return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)


# Support function
def filter_response(warranty):
    warranty = WarrantySerializer(warranty)
    warranty = warranty.data
    warranty['warrantyDate'] = warranty.pop('warranty_date')
    warranty["itemUid"] = warranty.pop("item_uid")
    del warranty['id'], warranty['comment']
    return warranty


def validWarranty(item_uid):
    try:
        return Warranty.objects.get(item_uid=item_uid)
    except Warranty.DoesNotExist:
        return False
