import signal
import pika
import requests
from circuitbreaker import circuit
from .functions import FunctionsWarranty
from .serializers import WarrantySerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

FAILURES = 3
TIMEOUT = 6


def startRabbit():
    parameters = pika.URLParameters(
        'amqps://waxtnnui:GqR1g_QZtwn9BuHIo0WhrWZ3pcxDpOzi@crow.rmq.cloudamqp.com/waxtnnui')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='warranty')

    def callback(ch, method, properties, receive):
        receive = receive.decode()
        requests.post('https://warranty-ivan.herokuapp.com/api/v1/warranty/{}'.format(receive))

    channel.basic_consume(queue='warranty', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


def signal_handler(signum, frame):
    raise Exception("Timed out!")


signal.signal(signal.SIGALRM, signal_handler)
signal.alarm(10)  # Ten seconds
try:
    startRabbit()
except Exception as e:
    print("Timed out!")


# API
@circuit(failure_threshold=FAILURES, recovery_timeout=TIMEOUT)
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
            if not request.data:
                warranty = dict(status='ON_WARRANTY', item_uid=item_uid, comment='None')
            else:
                data = request.data
                warranty = dict(status=data['status'], item_uid=item_uid,
                                comment=data['comment'], warrantyDate=data['warrantyDate'])
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


@circuit(failure_threshold=FAILURES, recovery_timeout=TIMEOUT)
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
