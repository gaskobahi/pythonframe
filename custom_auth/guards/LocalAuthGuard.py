import json
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed

from custom_auth.definitions.constants import AUTH_HEADER_TYPES
from custom_auth.services.auth_log_service import AuthLogService
from custom_auth.services.auth_service import AuthService
from user.services.user_service import UserService


User = get_user_model()

class LocalAuthGuard(BaseBackend):
    def __init__(self):
        authLogService= AuthLogService()
        self.authLogService = authLogService
    userService=UserService()
    def authenticate(self,request):
        authService = AuthService()
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            # Log auth request and save 'authLog' object to app request
            auth_log = self.authLogService.createFromRequest(
            request,
            username,
            settings.REQUEST_AUTH_METHOD_KEY
            )
            setattr(request,settings.REQUEST_AUTH_LOG_KEY,auth_log)
            #authService = AuthService(request)
            """
            Authentifie un utilisateur en fonction de critères personnalisés.
            """
            # Rechercher l'utilisateur (par défaut, avec le nom d'utilisateur)
            userLogged = json.loads(self.userService.authenticate(username,password))
            auth_user=authService.create_Auth_User_Form(userLogged,auth_log)
            setattr(request, settings.REQUEST_AUTH_USER_KEY, auth_user)

        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
    
    def authenticate_header(self, request):
        return AUTH_HEADER_TYPES  # example header
    
    
    
    
    def get_user(self, user_id):
        """
        Récupère un utilisateur à partir de son ID.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    def get_user_by_username(self, username):
        """
        Récupère un utilisateur à partir de son ID.
        """
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None