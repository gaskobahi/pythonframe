# myapp/models.py
from django.db import models

from base.models.base_core import BaseCoreEntity


class Category(BaseCoreEntity):
    name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name