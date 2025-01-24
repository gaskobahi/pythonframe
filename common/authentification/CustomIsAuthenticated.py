from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt

from custom_auth.definitions.constants import AUTH_HEADER_TYPES, AUTH_USER_JWT_HEADER
from custom_auth.models.BlacklistedToken import BlacklistedToken
from custom_auth.models.auth_log import AuthLog
from custom_auth.models.auth_user import AuthUser
from custom_auth.serializers.auth_user import AuthUserSerializer
from custom_auth.services.auth_service import AuthService
from user.models.user import User


class CustomIsAuthenticated(BasePermission):
    """
    Permission personnalisée pour vérifier l'authentification d'un utilisateur via un token personnalisé.
    """
    def has_permission(self, request, view):
        # Retrieve and validate the Authorization header
        auth_header = request.headers.get(AUTH_USER_JWT_HEADER)
        if not auth_header or not auth_header.startswith(AUTH_HEADER_TYPES):
            raise AuthenticationFailed("Token d'authentification manquant ou mal formaté.")

        # Extract the token
        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            raise AuthenticationFailed("Format de token invalide.")

        # Decode the JWT token
        try:
            decoded_token = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=settings.TOKEN_ALGORITHM,
                options={"verify_exp": True}  # Enable expiration verification
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Le token a expiré.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Token invalide.")

        # Verify the user ID in the token
        user_id = decoded_token.get(settings.TOKEN_USER_ID)
        if not user_id:
            raise AuthenticationFailed("L'ID utilisateur est manquant dans le token.")

        # Check if the token is blacklisted
        if BlacklistedToken.is_token_blacklisted(token):
            raise AuthenticationFailed("Le token est déjà blacklisté..")

        # Validate user existence
        try:
            #user = User.objects.get(id=user_id)
            #request.user = user
            user_session = decoded_token.get(settings.TOKEN_USER_SESSION)
            # Attach user to the request for further processing
            request.authUser = user_session
        except User.DoesNotExist:
            raise AuthenticationFailed("Utilisateur introuvable.")

        # Blacklist the token (optional, if needed)
        if  request.path == '/api/auth/logout/':
            BlacklistedToken.objects.create(token=token)
        
        #Process authLog from JWT
        authLog = AuthLog.objects.get(id=user_session.get('auth_log'))
        request.authLog=authLog
        if not authLog:
            raise AuthenticationFailed("Utilisateur introuvable.")
        else:
            self.checkAuthLog(authLog)
        
         #Process authUser from JWT
        authUser = AuthUser.objects.get(id=user_session.get('id'))
        authUserSerializer=AuthUserSerializer(authUser).data
        if  not authUserSerializer.get('is_active'):
            raise AuthenticationFailed("Session inactive")
        else:
            self.checkAuthUser(authUserSerializer)
        



        return True
        

    

    def checkAuthLog(self,authLog: AuthLog):
        if authLog.is_denied:
            raise AuthenticationFailed("Requête d'authentification non autorisée.")

    def checkAuthUser(self,authLog: AuthUser):
        if  not authLog.get('user').get('is_active'):
            raise AuthenticationFailed("Compte inactif")
