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
        if valid_warranty(item_uid):
            warranty = valid_warranty(item_uid)
            filterRes = filter_response(warranty)
            return JsonResponse(filterRes, status=status.HTTP_200_OK, safe=False)
        return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        if valid_warranty(item_uid):
            warrantyDelete = valid_warranty(item_uid)
            warrantyDelete.delete()
            return JsonResponse(1, status=status.HTTP_204_NO_CONTENT, safe=False)
        return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def request_warranty(request, item_uid):
    if valid_warranty(item_uid):
        instWarranty = warrantyData = valid_warranty(item_uid)
        warrantyData = WarrantySerializer(warrantyData).data
        parseDict = JSONParser().parse(request)
        if 'reason' in parseDict:
            warrantyData['comment'] = parseDict['reason']
        decision = dict(warrantyDate=warrantyData['warranty_date'] )
        if warrantyData['status'] == 'ON_WARRANTY':
            warrantyData['status'] = 'USE_WARRANTY'
            warranty_serializer = WarrantySerializer(instance=instWarranty, data=warrantyData)
            if warranty_serializer.is_valid():
                warranty_serializer.save()
            if parseDict['availableCount'] > 1:
                decision['decision'] = 'RETURN'
            else:
                decision['decision'] = 'FIXING'
        else:
            decision['decision'] = 'REFUSED'
        return JsonResponse(decision, status=status.HTTP_200_OK)
    return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)


# Support function
def filter_response(warranty):
    warranty = WarrantySerializer(warranty).data
    warranty['warrantyDate'] = warranty.pop('warranty_date')
    warranty["itemUid"] = warranty.pop("item_uid")
    del warranty['id'], warranty['comment']
    return warranty


def valid_warranty(item_uid):
    try:
        return Warranty.objects.get(item_uid=item_uid)
    except Warranty.DoesNotExist:
        return False
