from rest_framework import serializers

from custom_auth.definitions.constants import REQUEST_AUTH_USER_KEY
from custom_auth.services.auth_service import AuthService

class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        authService = AuthService(self)
        username = data.get('username')
        password = data.get('password')
        user = authService.validateUser(username,password)

        """
        if not user:
            raise serializers.ValidationError({'mesage':"Sidibe Nom d'utilisateur ou mot de passe invalide."})
        else:
            if user and not user.is_active:
                raise InvalidToken({'mesage':" Votre compte est désactivé."})
         # Add standard claims to the JWT payload
        """
        data[REQUEST_AUTH_USER_KEY] = user
        return data
    
