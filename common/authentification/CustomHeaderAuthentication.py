from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import json

from user.models.user import User

class CustomHeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        Méthode pour récupérer et valider le header X-User-Claims.
        """
        # Récupérer la valeur du header X-User-Claims
        user_claims = request.headers.get('X-User-Claims')
        if not user_claims:
            raise AuthenticationFailed('Le header X-User-Claims est manquant.')

        try:
            # Décodez le JSON (si vous avez des claims encodés en JSON)
            claims = json.loads(user_claims)

            # Par exemple, récupérer l'ID de l'utilisateur
            user_id = claims.get('user')
            if not user_id:
                raise AuthenticationFailed('Le champ user_id est manquant dans X-User-Claims.')

            # Vérifier si l'utilisateur existe dans la base de données
            user = User.objects.get(id=user_id)

        except (ValueError, KeyError, User.DoesNotExist) as e:
            raise AuthenticationFailed('Impossible de valider les informations d\'utilisateur : {}'.format(e))

        return (user, None)  # Retourne l'utilisateur authentifié et None pour le token (non utilisé ici)