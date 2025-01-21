from django.utils.deprecation import MiddlewareMixin

from custom_auth.guards.request_issuer_guard import RequestIssuerGuard

class ApplicationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        guard = RequestIssuerGuard()
        if not guard.has_permission(request, None):  # Vérifiez les permissions
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Permission refusée.")
        return None