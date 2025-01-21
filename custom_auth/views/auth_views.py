from django.conf import settings
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed

from common.authentification.CustomIsAuthenticated import CustomIsAuthenticated
from custom_auth.guards.LocalAuthGuard import LocalAuthGuard
from custom_auth.services.auth_service import AuthService
from user.models.user import User


# Customizing the token response if needed
class LoginView(APIView):
    authentication_classes = [LocalAuthGuard]
    def post(self, request):
        try:
            authService=AuthService(request)
            return authService.ConfirmLogin(getattr(request,settings.REQUEST_AUTH_USER_KEY,None))
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found') 
        except Exception as e:
            # Handle other unexpected exceptions
            authLog=getattr(request,settings.REQUEST_AUTH_LOG_KEY,None)
                # Access the AuthLog related to the user
            if authLog is not None:
                authLog.denial_reason = str(e)
                authLog.save()
            raise AuthenticationFailed(f"Authentication failed: {str(e)}")
        
    
class LogoutAPIView(APIView):
    permission_classes = [CustomIsAuthenticated]
    def post(self, request, *args, **kwargs):
        authService=AuthService(request)
        return authService.logout()
       


