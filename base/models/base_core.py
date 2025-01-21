# myapp/models.py
from typing import Any, Dict
import uuid
from django.db import models


class BaseCoreEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by_id = models.UUIDField(null=True, blank=True)
    updated_by_id = models.UUIDField(null=True, blank=True)
    deleted_by_id = models.UUIDField(null=True, blank=True)
    class Meta:
        abstract = True
        







