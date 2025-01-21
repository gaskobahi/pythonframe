import json

from django.forms import ValidationError
from custom_auth.models.auth_user import AuthUser
from user.models.user import User
from rest_framework.exceptions import AuthenticationFailed

from user.serializers.user import UserSerializer, custom_serializer


class UserService:

    def authenticate(self, username: str, password: str):
        """
        Authentifie un utilisateur avec un nom d'utilisateur et un mot de passe.
        """
        # Recherche l'utilisateur avec des relations spécifiques (si besoin)
        try:
            user =  User.objects.get(username=username)
        except User.DoesNotExist:
            # Lève une exception si l'utilisateur n'existe pas
            raise AuthenticationFailed({"username": ["Nom d'utilisateur ou mot de passe incorrect"]})
        
        # Vérifie le mot de passe
        if not user.check_password(password):
            raise AuthenticationFailed({"password": ["Nom d'utilisateur ou mot de passe incorrect"]})
        
        if not user:
            raise AuthenticationFailed({'mesage':"Nom d'utilisateur ou mot de passe invalide."})
        else:
            if user and not user.is_active:
                raise AuthenticationFailed({'mesage':" Votre compte est désactivé."})
         # Add standard claims to the JWT payload
        
        # Convertit l'utilisateur en un objet utilisateur adapté à l'authentification
        return self.to_auth_user(user)

    def to_auth_user(self, user):
      # Fetch the user object from the database
        user_instance = User.objects.get(id=user.id)
        # Serialize the user instance
        serializer = UserSerializer(user_instance)
        # Return the serializer data as a dictionary
        return json.dumps(serializer.data, default=custom_serializer)
            # Ajoutez d'autres champs nécessaires pour votre réponse
    
    def get_client_ip(request):
        print('x_forwarded_for',request)
    # Check for the X-Forwarded-For header, commonly set by proxies/load balancers
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        print('x_forwarded_for',x_forwarded_for)
        if x_forwarded_for:
            # It may contain multiple IPs, the first one is the client's real IP
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            # Fallback to REMOTE_ADDR for the direct client IP
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_user_data(authUser):
        """
        Return user data serialized with the UserSerializer.
        """
        # Fetch the user object from the database
        user_instance = User.objects.get(id=authUser.id)
        # Serialize the user instance
        serializer = UserSerializer(user_instance)
        # Return the serializer data as a dictionary
        return json.dumps(serializer.data, default=custom_serializer)

    def  checkAuthUser(authUser: AuthUser):
            if not authUser.get('is_active'):
                raise AuthenticationFailed({"Session inactive": 'Session inactive'})
    
    def change_password(self,data):
        userService=UserService()
        if not userService.check_password(data['current_password']):
            raise ValidationError({'current_password': ['Mot de passe actuel incorrect']})
        print('azaaza',data['password'])
        return User.set_new_password(data['password'])
       
       

    def check_password(self,password: str) -> bool:
            print('sdsdsds',password)
            #return User.check_password(password)
            return True
    """
    def change_password(self,data):
        if not self.check_password(data['current_password']):
            raise ValidationError({'current_password': ['Mot de passe actuel incorrect']})
        print('azaaza',data['password'])
        return User.set_new_password(data['password'])
    """
