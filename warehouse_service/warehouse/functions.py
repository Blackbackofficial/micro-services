from uuid import UUID
import re


class FunctionsWarehouse:
    """
    Support function for warehouse service
    """

    def regularExp(self, types):
        """
        Validation of data from JSON(request) using a pattern from regular expressions.
        1) Type 1 for data with model & size 2) Type 2 for comment in 'reason'
        :param self: from function in JSON(request)
        :return: True or False
        """

        model = '^[A-Z]+[a-z 0-9]+$'
        size = '^[A-Z]+$'
        reason = '^[A-Z][a-z 0-9]+$'
        if types == 1 and (re.match(model, self.get("model")) and re.match(size, self.get("size"))) is not None:
            return True
        if types == 2 and re.match(reason, self.get("reason")) is not None:
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
