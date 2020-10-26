import uuid

from django.db import models


class Store(models.Model):
    name = models.CharField('Имя', max_length=20, blank=False, help_text="Enter field name")
    user_uid = models.UUIDField(default=uuid.uuid4, editable=True)
