import re
from .models import Warranty
from .serializers import WarrantySerializer


class FunctionsWarranty:
    """
    Support function for warranty service
    """

    def filter_response(self):
        """
        Sorts the response, removes unnecessary data. Two exits when a specific user order and when all user orders.
        :param self: dict all user orders
        :return: reformed warranty
        """

        data = WarrantySerializer(self).data
        data['warrantyDate'] = data.pop('warranty_date')
        data["itemUid"] = data.pop("item_uid")
        del data['id']
        return data

    def valid_warranty(self):
        """
        Check for existence warranty Uid.
        :param self: User Uid
        :return: warranty Uid or False
        """

        try:
            return Warranty.objects.get(item_uid=self)
        except Warranty.DoesNotExist:
            return False

    def regularExp(self):
        """
        Validation of data from JSON(request) using a pattern from regular expressions.
        1) Type 1 for data with model & size 2) Type 2 for comment in 'reason'
        :param self: from function in JSON(request)
        :return: True or False
        """

        availableCount = '^[0-9]+$'
        reason = '^[A-Z][a-z 0-9]+$'
        if (re.match(availableCount, str(self.get("availableCount"))) and re.match(reason, self.get(
                "reason"))) is not None:
            return True
        return False
