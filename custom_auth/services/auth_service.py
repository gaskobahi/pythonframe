from datetime import datetime
import json
import uuid
from django.conf import settings
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from common.abilities.abilities import define_abilities_for
from custom_auth.models.auth_log import AuthLog
from custom_auth.models.auth_user import AuthUser
from custom_auth.serializers.auth_user import AuthUserSerializer
from custom_auth.strategies.customTokens import CustomToken
from user.models.user import User
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from custom_auth.middleware.RequestMiddleware import get_current_request

from user.serializers.user import UserSerializer

def custom_serializer(obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")


class AuthService:
    def __init__(self):

        self.request=get_current_request()
    def validateUser(self,authUser):
        #authLog = this.request[REQUEST_AUTH_LOG_KEY] as AuthLog;
        authUser = json.loads(authUser)

        # Check authLog status
        # this.checkAuthLog(authLog);
        current_time = datetime.now()
        if authUser:
            #authUser.authLogId = authLog?.id;
            #authUser.authLog = authLog;
            authUser["last_access_date"] = current_time
            authUser["userAgent"] = self.request.headers.get('User-Agent')
            authUser["ip_address"] = self.get_client_ip(self.request)
            #Check user status
            return authUser
  
    def create_Auth_User_Form(self,userLogged:User,authLog:AuthLog):
        application = self.request.META.get(settings.REQUEST_APP_KEY)  # Les headers HTTP sont en MAJUSCULES et préfixés par "HTTP_"
        #Create authUser

        auth=AuthUser.objects.create(
            username=userLogged.get('username'),
            role_id=str(userLogged.get('role_id')),
            is_active=userLogged.get('is_active'),
            application_id=application.get('id'),
            user_agent=self.get_userAgent(),
            ip_address=self.get_client_ip(),
            user_data=userLogged,
            last_access_date=datetime.now(),
            auth_log_id=authLog.id,
            user_id=userLogged.get('id')
        )
        return auth
        
    def create_authLog(self,user):
        user = json.loads(user)
        auth_log = AuthLog.objects.create(
            application_id=self.get_applicationId(self.request),
            ip_address=self.get_client_ip(self.request),
            username=user.get('username'),
            request_url=self.request.build_absolute_uri(),
            request_method=self.request.method,
            user_agent=self.get_userAgent(self.request),
            user_data=user
        )
        return auth_log
    
    def ConfirmLogin(self,loggedUser,authLog):
        authUser =loggedUser
        #Create authUser
        authUser.created_by_id = authUser.id
        authUser:AuthUser =self.save_and_return(authUser)
        # Update authUser
        authUser.updated_by_id = authUser.id
        #authUser =  authUser.save()
        authUser:AuthUser =self.save_and_return(authUser)
        #Reload auth user data
        authUser=json.loads(self.getCurrentUser(authUser)) 
        #authUserSerial=AuthUserSerializer(authUser)
        #Update request auth data
        setattr(self.request,settings.REQUEST_AUTH_LOG_KEY,authLog) 
        setattr(self.request,settings.REQUEST_AUTH_USER_KEY,authUser)

        refresh = CustomToken.for_user(self.request,authUser,authLog)
        session = authUser 
        user = User.objects.get(id=authUser.get('user_id'))
        _user= UserSerializer(user)

        # Update last authentication
        user.last_access_id = authUser.get('id')
        setattr(self.request,settings.SIMPLE_JWT.get('USER_ID_CLAIM'),_user.data)
        #get user ability
        abilities = define_abilities_for(authUser.get('user'))

        user.save();
        return Response({
            #'refresh': str(refresh),
            'session':session,
            'abilities':abilities['can'],     
            'token':str(refresh)
        }, status=status.HTTP_200_OK)

    def logout(self,authUser):
        print('trtrtr',authUser)
        authUser:AuthUser = AuthUser.objects.get(id=authUser.get('id'))
        if authUser.hasId():
            authUser.is_active = False
            authUser.logout_at = datetime.now()
            authUser.logout_by_id = authUser.id
            authUser.save()
            return Response({'detail': 'Déconnexion réussie.'}, status=status.HTTP_200_OK)

   
        #if not authUser['user']:
           # raise AuthenticationFailed({"Compte inactif": 'Compte inactif'})
   
    def get_client_ip(self):
        """
        Extract the client's IP address from the request object.
        """
        # Check for the X-Forwarded-For header, commonly set by proxies/load balancers
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            # It may contain multiple IPs, the first one is the client's real IP
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            # Fallback to REMOTE_ADDR for the direct client IP
            ip = self.request.META.get("REMOTE_ADDR")
        return ip
    
    def get_applicationId(self):
        application = self.request.META.get(settings.REQUEST_APP_KEY)  # Les headers HTTP sont en MAJUSCULES et préfixés par "HTTP_"
        applicationId=application.get('id')
        return applicationId
    
    def get_userAgent(self):
        userAgent=self.request.META[settings.REQUEST_CLIENT_ID_HEADER]
        return userAgent
     
    def check_auth_user(auth_user):
        if not auth_user.is_active:
            raise PermissionDenied("Session inactive")
        if not getattr(auth_user.user, 'is_active', False):
            raise PermissionDenied("Compte inactif")
    
    def create_Auth_from_request(self,user:AuthUser):
        user = User.objects.get(id=user.id)
        auth_log = AuthLog.objects.create(
            application_id=self.get_applicationId(),
            ip_address=self.get_client_ip(),
            username=user.username,
            request_url=self.request.build_absolute_uri(),
            request_method=self.request.method,
            user_agent=self.get_userAgent(),
            **user  # Allows other fields in dto to populate the model
        )
        return auth_log
    

  
    def getCurrentUser(self,authUser):
        return self.getSession(authUser)
    


    def getSession(self,authUser):
        requestAuthUser:AuthUser = authUser or getattr(self.request,settings.REQUEST_AUTH_USER_KEY,None) 
        return self.to_auth_user(requestAuthUser)
    
   


    def to_auth_user(self, user):
      # Fetch the user object from the database
        authuser_instance = AuthUser.objects.get(id=user.id)
        # Serialize the user instance
        serializer = AuthUserSerializer(authuser_instance)
        # Return the serializer data as a dictionary
        return json.dumps(serializer.data, default=custom_serializer)

  

    def save_and_return(self,instance):
        instance.save()  # Sauvegarde l'instance dans la base de données
        return instance 