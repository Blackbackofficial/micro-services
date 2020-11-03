from django.db import models
import uuid


class Items(models.Model):
    available_count = models.IntegerField(blank=True, null=True, default='')
    model = models.CharField(max_length=50, blank=False, default='')
    size = models.CharField(max_length=50, blank=False, default='')


class Order_item(models.Model):
    canceled = models.BooleanField(default=False)
    order_item_uid = models.UUIDField(default=uuid.uuid4, editable=True)
    order_uid = models.UUIDField(default=uuid.uuid4, editable=True)
    item_id = models.IntegerField(blank=True, null=True, default='')
