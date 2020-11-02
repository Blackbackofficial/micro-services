from django.utils import timezone
from django.db import models
import uuid


class Warranty(models.Model):
    comment = models.CharField('Коммент', max_length=100, blank=False)
    item_uid = models.UUIDField(default=uuid.uuid4, editable=True)
    status = models.CharField('status', max_length=30, blank=False)
    warranty_date = models.DateTimeField(default=timezone.now)
