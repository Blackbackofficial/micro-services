from django.db import models
import uuid


class Store(models.Model):
    name = models.CharField('Имя', max_length=20, blank=False)
    user_uid = models.UUIDField(default=uuid.uuid4, editable=True)
