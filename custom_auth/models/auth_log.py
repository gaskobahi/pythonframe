import uuid
from django.db import models

from common.models.core_entity import CoreEntity


class AuthLog(CoreEntity):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, verbose_name=("Nom d'utilisateur"))
    request_url = models.JSONField(verbose_name=("Requete Url"))
    request_method = models.CharField(max_length=255, verbose_name=("Requete Methode"))
    is_denied = models.BooleanField(default=False, verbose_name=("Is denied"))
    denial_reason = models.CharField(max_length=255, verbose_name=("Denial Reason"))
    auth_method = models.CharField(max_length=255, verbose_name=("auht Method"))
    ip_address = models.GenericIPAddressField(null=True, verbose_name=("Adresse IP"))
    last_access_date = models.DateTimeField(null=True, verbose_name=("Dernière date d'accès"))
    user_agent = models.JSONField(null=True, verbose_name=("Agent utilisateur"))
    application_id = models.CharField(max_length=255, verbose_name=("Application ID"))
    
    def __str__(self):
        return self.username
    
    
    class Meta:
        app_label = 'custom_auth' 