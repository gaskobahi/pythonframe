from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from custom_auth.views.auth_views import LoginView, LogoutAPIView
from custom_auth.views.change_password_view import ChangePasswordView

urlpatterns = [
    path('auth/token/', LoginView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),
    path('auth/change_password/', ChangePasswordView.as_view(), name='change_password'),
    
]