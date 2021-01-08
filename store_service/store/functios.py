"""
Support function for store service
"""
from urllib.error import HTTPError
from uuid import UUID
from django.core.exceptions import ValidationError
from .models import Store
from urllib.request import urlopen
import re


def filter_response(storeReq):
    """
    Sorts the response, removes unnecessary data. Two exits when a specific user order
    and when all user orders, always returns storeReq
    """
    if type(storeReq) is dict:
        storeReq['date'] = storeReq['orderDate']
        storeReq['warrantyStatus'] = storeReq['status']
        del storeReq['itemUid'], storeReq['status'], storeReq['orderDate'], storeReq['id'], storeReq['available_count']
    else:
        for item in storeReq:
            if 'date' and 'warrantyStatus' and 'itemUid' in item:
                item['date'] = item['orderDate']
                item['warrantyStatus'] = item['status']
                del item['itemUid'], item['status'], item['orderDate']
            if 'id' in item:
                del item['id']
            if 'available_count' in item:
                del item['available_count']
    return storeReq


def validUser(user_uid):
    """
    Check for existence User Uid, return user_uid or False
    """
    try:
        return Store.objects.get(user_uid=user_uid)
    except ValidationError:
        return False


def regularExp(request):
    """
    Validation of data from JSON(request) using a pattern from regular expressions
    """
    model = '^[A-Z]+[a-z 0-9]+$'
    size = '^[A-Z]+$'
    if (re.match(model, request.get("model")) and re.match(size, request.get("size"))) is not None:
        return True
    return False


def pingServices():
    """
    Checking the health of other services, return True or False
    """
    try:
        urlopen("https://warranty-ivan.herokuapp.com/manage/health/")
        urlopen("https://warehouse-ivan.herokuapp.com/manage/health/")
        urlopen('https://orders-ivan.herokuapp.com/manage/health/')
        return True
    except HTTPError:
        return False


def validate_uuid4(uuid_string):
    """
    Validation uuid from string URL or in JSON, return True or False
    """
    try:
        UUID(uuid_string, version=4)
    except ValueError:
        return False
    return True
