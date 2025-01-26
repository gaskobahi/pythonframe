from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def is_admin(view_func):
    """
    Décorateur pour vérifier que l'utilisateur est un administrateur.
    """
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_staff:  # Si l'utilisateur n'est pas un admin
            return Response(
                {"detail": "Vous devez être un administrateur pour accéder à cette ressource."},
                status=status.HTTP_403_FORBIDDEN
            )
        return view_func(self, request, *args, **kwargs)
    
    return wrapper