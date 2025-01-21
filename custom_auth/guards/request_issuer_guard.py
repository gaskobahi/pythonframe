from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from custom_auth.definitions.constants import DEFAULT_APPLICATION_ID, IS_PUBLIC_META_KEY, REQUEST_APP_ID_HEADER, REQUEST_APP_KEY, REQUEST_CLIENT_ID_HEADER

class RequestIssuerGuard(BasePermission):
    """
    Garde permettant de vérifier l'accès basé sur l'identifiant de l'application (application-id).
    """
    def has_permission(self, request, view):
        # Vérification des ressources publiques
        is_public = getattr(view, IS_PUBLIC_META_KEY, False)
        if is_public:
            return True

        # Récupération de l'identifiant de l'application depuis les en-têtes
        application_id = request.headers.get(REQUEST_APP_ID_HEADER, DEFAULT_APPLICATION_ID)

        if not application_id:
            raise PermissionDenied("L'identifiant de l'application est manquant.")

        # Ajout de 'applicationId' dans l'objet request
        request.META[REQUEST_APP_KEY] = {"id": application_id}
        request.META[REQUEST_CLIENT_ID_HEADER] =request.headers.get('User-Agent')

        return True