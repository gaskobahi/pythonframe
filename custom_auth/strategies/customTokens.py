from datetime import datetime, timedelta
import json
from django.conf import settings
import jwt
from rest_framework_simplejwt.tokens import RefreshToken

from custom_auth.serializers.auth_user import AuthUserSerializer
from custom_auth.services.auth_log_service import AuthLogService

class CustomToken(RefreshToken):
    @classmethod
    def for_user2(cls, user):
        """
        Personnalise le contenu du token JWT.
        """
        # Créer le token avec la méthode parente
        token = super().for_user(user)
        token = jwt.encode(user, settings.JWT_SECRET_KEY, algorithm='HS256')
        session = AuthUserSerializer(user)
        token['session'] = session.data
        token['session']['user'] = user.user_data        
        return token


    def for_user(request,authUser,authLog):
        application = request.META.get(settings.REQUEST_APP_KEY) 
        userAgent=request.META[settings.REQUEST_CLIENT_ID_HEADER]
        #Create auth JWT
        # Créer un dictionnaire pour le payload
        payload = {
            settings.TOKEN_USER_ID: str(authUser.get('user_id')),  # Inclure l'ID de l'utilisateur
            'jti': str(authUser.get('id')),
            'sub':str(authUser.get('id')),
            'username':str(authUser.get('username')),
            #'aud': application.get('id'),
            'iat': datetime.now(),
            'exp':datetime.now()+settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME'),  # Expiration du token
            #'ip': authLogService.get_client_ip(request),
            'ip': authLog.ip_address,
            'iss': application.get('id'),
        }
        # Ajouter des données supplémentaires au payload avant l'encodage
        #session_data = AuthUserSerializer(authUser).data  # Sérialiser l'utilisateur
        payload['session'] = authUser
        #payload['session']['user'] = authUser.get('user_data')  # Ajouter des données supplémentaires à la session
        # Encoder le token avec le payload sous forme de dictionnaire
        token = jwt.encode(payload,settings.JWT_SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)
        return token