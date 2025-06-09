import uuid

from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
