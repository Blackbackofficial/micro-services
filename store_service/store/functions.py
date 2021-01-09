from urllib.error import HTTPError
from uuid import UUID
from django.core.exceptions import ValidationError
from .models import Store
from urllib.request import urlopen
import re


class FunctionsStore:
    """
    Support function for store service
    """

    @staticmethod
    def pingServices():
        """
        Checking the health of other services.
        :return: True or False
        """

        try:
            urlopen("https://warranty-ivan.herokuapp.com/manage/health/")
            urlopen("https://warehouse-ivan.herokuapp.com/manage/health/")
            urlopen('https://orders-ivan.herokuapp.com/manage/health/')
            return True
        except HTTPError:
            return False

    def pingDegradation(self):
        """
        Checking the health of other services.
        :return: True or False
        """

        try:
            urlopen('{}'.format(self))
            return True
        except HTTPError:
            return False

    def filter_response(self):
        """
        Sorts the response, removes unnecessary data. Two exits when a specific user order and when all user orders.
        :param self: dict one user order or all user orders
        :return: reformed storeReq
        """

        key = {'itemUid', 'status', 'orderDate', 'id', 'available_count'}
        if type(self) is dict:
            self['date'] = self['orderDate']
            self['warrantyStatus'] = self['status']
            i = 0
            for item in key:
                if item in self.keys():
                    del self[item]
        else:
            for item in self:
                if 'date' and 'warrantyStatus' and 'itemUid' in item:
                    item['date'] = item['orderDate']
                    item['warrantyStatus'] = item['status']
                    del item['itemUid'], item['status'], item['orderDate']
                if 'id' in item:
                    del item['id']
                if 'available_count' in item:
                    del item['available_count']
        return self

    def validUser(self):
        """
        Check for existence User Uid.
        :param self: User Uid
        :return: user_uid or False
        """

        try:
            return Store.objects.get(user_uid=self)
        except ValidationError:
            return False
        except Store.DoesNotExist:
            return False

    def regularExp(self):
        """
        Validation of data from JSON(request) using a pattern from regular expressions
        :param self: from function in JSON(request)
        :return: True or False
        """

        model = '^[A-Z]+[a-z 0-9]+$'
        size = '^[A-Z]+$'
        if (re.match(model, self.get("model")) and re.match(size, self.get("size"))) is not None:
            return True
        return False

    def validate_uuid4(self):
        """
        Validation uuid from string URL or in JSON.
        :param self: User or Order Uid
        :return: True or False
        """

        try:
            UUID(self, version=4)
        except ValueError:
            return False
        return True
