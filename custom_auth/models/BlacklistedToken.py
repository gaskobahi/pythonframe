import uuid
from django.db import models

class BlacklistedToken(models.Model):
    """
    Modèle pour les tokens révoqués.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.TextField(verbose_name="Token JWT", unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def is_token_blacklisted(token):
        try:
            BlacklistedToken.objects.get(token=token)
            return True  # Le token est blacklisté
        except BlacklistedToken.DoesNotExist:
            return False  # Le token n'est pas blacklisté


    def __str__(self):
        return f"BlacklistedToken(id={self.id}, created_at={self.created_at})"