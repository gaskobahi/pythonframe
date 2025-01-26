from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def is_owner(view_func):
    """
    Décorateur pour vérifier que l'utilisateur ne peut modifier que son propre profil.
    """
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        user_id = request.user.id  # ID de l'utilisateur authentifié
        profile_id = kwargs.get('pk')  # ID du profil dans l'URL

        # Vérifie si l'utilisateur modifie son propre profil
        if str(user_id) != str(profile_id):
            return Response(
                {"detail": "Vous n'avez pas la permission de modifier ce profil."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Appelle la vue si la condition est remplie
        return view_func(self, request, *args, **kwargs)
    
    return wrapper