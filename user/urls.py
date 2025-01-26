from rest_framework.routers import DefaultRouter
# myproject/urls.py
from django.urls import path


from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from user.views.role import RoleDetailView, RoleListCreateView
from user.views.user import UserDetailView, UserListCreateView
router = DefaultRouter()
URIROLE='role/'
URIUSER='user/'

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Documentation de l'API",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="bahiboris@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path('role/', RoleListCreateView.as_view(), name='role-list-create'),
    path('role/<uuid:pk>/', RoleDetailView.as_view(), name='role-detail'),

    path('user/', UserListCreateView.as_view(), name='user-list-create'),
    path('user/<uuid:pk>/', UserDetailView.as_view(), name='user-detail'),

    

   
]