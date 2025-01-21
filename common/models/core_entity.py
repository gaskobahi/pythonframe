import uuid
from django.db import models

from base.models.base_core import BaseCoreEntity


class CoreEntity(BaseCoreEntity):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_by = models.ForeignKey(
        'AuthUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_core_entities",
        verbose_name=("Créé par"),
    )
    updated_by = models.ForeignKey(
        'AuthUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_core_entities",
        verbose_name=("Mis à jour par"),
    )
    deleted_by = models.ForeignKey(
        'AuthUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name="deleted_core_entities",
        verbose_name=("Supprimé par"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=("Date de création"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=("Date de mise à jour"))
    class Meta:
        abstract = True
