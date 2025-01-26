from rest_framework.permissions import BasePermission

from base.enums import AbilityActionEnum

class IsOwnerPermission(BasePermission):
    """
    Permission qui permet uniquement à un utilisateur de modifier son propre profil.
    """
    def has_permission(self, request, view):
        # L'action 'edit' est autorisée uniquement si l'utilisateur modifie son propre profil
        if view.action == AbilityActionEnum.edit:
            user_id = request.user.id  # ID de l'utilisateur authentifié
            profile_id = view.kwargs.get('pk')  # Récupère l'ID du profil depuis l'URL
            return str(user_id) == str(profile_id)

        # Autoriser d'autres actions comme 'read'
        return True