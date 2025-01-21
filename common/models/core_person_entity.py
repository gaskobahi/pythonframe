from base.models.base_core import BaseCoreEntity
from django.db import models


class PersonCoreEntity(BaseCoreEntity):
    first_name = models.CharField(('Prénoms'), max_length=100, null=True, blank=True)
    last_name = models.CharField(('Nom'), max_length=100, null=True, blank=True)
    phone_number = models.CharField(('Numéro de téléphone'), max_length=15, null=True, blank=True)
    email = models.EmailField(('Email'), null=True, blank=True)
    address = models.CharField(('Adresse'), max_length=255, null=True, blank=True)
    class Meta:
        abstract = True
