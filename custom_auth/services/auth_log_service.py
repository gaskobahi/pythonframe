from django.conf import settings
from custom_auth.models.auth_log import AuthLog

class AuthLogService:

    def get_client_ip(self,request):
            """
            Extract the client's IP address from the request object.
            """
            # Check for the X-Forwarded-For header, commonly set by proxies/load balancers
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            if x_forwarded_for:
                # It may contain multiple IPs, the first one is the client's real IP
                ip = x_forwarded_for.split(",")[0].strip()
            else:
                # Fallback to REMOTE_ADDR for the direct client IP
                ip = request.META.get("REMOTE_ADDR")
            return ip
    


        #Log auth request and save 'authLog' object to app request
    def createFromRequest(self,request,username,authMethod):
        application = request.META.get(settings.REQUEST_APP_KEY) 
        userAgent=request.META[settings.REQUEST_CLIENT_ID_HEADER]
        auth_log = AuthLog.objects.create(
            application_id=application.get('id'),
            ip_address=self.get_client_ip(request),
            username= username or request.get('user').get('username'),
            request_url=request.build_absolute_uri(),
            request_method=request.method,
            auth_method=authMethod,
            user_agent=userAgent
        )

        return auth_log
    
    