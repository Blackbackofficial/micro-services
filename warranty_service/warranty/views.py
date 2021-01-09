from .functions import FunctionsWarranty
from .serializers import WarrantySerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view


# API
@api_view(['GET', 'POST', 'DELETE'])
def actions_warranty(request, item_uid):
    """
    GET /api/v1/warranty/{itemUid} - information about the warranty status.
    POST /api/v1/warranty/{itemUid} - request for the beginning of the warranty period.
    DELETE /api/v1/warranty/{itemUid} - request to close the warranty.
    :param request: request to determine GET/POST/DELETE
    :param item_uid: Item Uid
    :return: 1) save and 204 2) get warranty on item_uid 3) delete and 204
    """

    try:
        if request.method == 'POST':
            warranty = dict(status='ON_WARRANTY', item_uid=item_uid, comment='None')
            warranty_serializer = WarrantySerializer(data=warranty)
            if warranty_serializer.is_valid():
                warranty_serializer.save()
                return JsonResponse(1, status=status.HTTP_204_NO_CONTENT, safe=False)

        if request.method == 'GET':
            if FunctionsWarranty.valid_warranty(item_uid):
                warranty = FunctionsWarranty.valid_warranty(item_uid)
                filterRes = FunctionsWarranty.filter_response(warranty)
                return JsonResponse(filterRes, status=status.HTTP_200_OK, safe=False)

        if request.method == 'DELETE':
            if FunctionsWarranty.valid_warranty(item_uid):
                warrantyDelete = FunctionsWarranty.valid_warranty(item_uid)
                warrantyDelete.delete()
                return JsonResponse(1, status=status.HTTP_204_NO_CONTENT, safe=False)
        return JsonResponse({'message': 'The tutorial does not exist or No Content'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def request_warranty(request, item_uid):
    """
    POST /api/v1/warranty/{itemUid}/warranty – Warranty decision request.
    :param request: JSON hidden in the data in request
    :param item_uid: Item Uid
    :return: changes ON_WARRANTY to USE_WARRANTY and returns RETURN or FIXING
    """

    try:
        if FunctionsWarranty.valid_warranty(item_uid):
            instWarranty = warrantyData = FunctionsWarranty.valid_warranty(item_uid)
            warrantyData = WarrantySerializer(warrantyData).data
            parseDict = request.data

            if FunctionsWarranty.regularExp(parseDict) is False:
                return JsonResponse({'message': 'Is not valid reason or count'}, status=status.HTTP_406_NOT_ACCEPTABLE)

            if 'reason' in parseDict:
                warrantyData['comment'] = parseDict['reason']
            decision = dict(warrantyDate=warrantyData['warranty_date'])

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
    except Exception as e:
        return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)
