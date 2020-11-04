import uuid
from django.db import models
from django.utils import timezone


class Orders(models.Model):
    item_uid = models.UUIDField(default=uuid.uuid4, editable=True)
    order_date = models.DateTimeField(default=timezone.now)
    order_uid = models.UUIDField(default=uuid.uuid4, editable=True)
    status = models.CharField(max_length=20, blank=False)
    user_uid = models.UUIDField(default=uuid.uuid4, editable=True)
