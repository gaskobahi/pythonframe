import uuid
from django.db import models

from base.models.base_core import BaseCoreEntity
from custom_auth.models.auth_log import AuthLog
from user.models.role import Role
from django.apps import apps  # Import dynamique des modèles

from user.models.user import User


class AuthUser(BaseCoreEntity):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, verbose_name=("Nom d'utilisateur"))
    is_active = models.BooleanField(default=False, verbose_name=("Validité"))
    ip_address = models.GenericIPAddressField(null=True, verbose_name=("Adresse IP"))
    last_access_date = models.DateTimeField(null=True, verbose_name=("Dernière date d'accès"))
    user_agent = models.JSONField(null=True, verbose_name=("Agent utilisateur"))
    user_data = models.JSONField(verbose_name=("Données de l'utilisateur"))
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="auth_users",verbose_name=("Dernier accès"))

    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        related_name="auth_users",
        verbose_name=("Role d'un utilisateur front office"),
    )
    auth_log = models.ForeignKey(
        AuthLog,
        on_delete=models.SET_NULL,
        null=True,
        related_name="auth_users",
        verbose_name=("Auth log user"),
    )   
    application_id = models.CharField(max_length=255, verbose_name=("Application ID"))
    logout_at = models.DateTimeField(null=True, verbose_name=("Date de déconnexion"))
    logout_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        related_name="logout_users",
        verbose_name=("Déconnecté par"),
    )

    def hasId(self):
        return self.id is not None
    
    def __str__(self):
        return self.username
    
    
    class Meta:
        app_label = 'custom_auth' 