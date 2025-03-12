from rest_framework.routers import DefaultRouter
# myproject/urls.py
from django.urls import path

from ecc.views.ecc import EccListCreateView

from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from ecc.views.stock_analysis import StockMovementView
from ecc.views.temp_ecc import TempEccListCreateView

router = DefaultRouter()

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
    path('ecc/', EccListCreateView.as_view(), name='ecc-list-create'),

    path('ecc/stockmovement/', StockMovementView.get_stockmovement, name='ecc-stockmovement'),
    path('ecc/bypackagelot/', StockMovementView.get_mvt_by_package_lot_number, name='ecc-get_mvt_by_package_lot_number'),
    path('ecc/byvariantcode/', StockMovementView.get_mvt_by_variant_code, name='ecc-get_mvt_by_variant_code'),


    path('tempecc/', TempEccListCreateView.as_view(), name='ecc-list-create'),



    # Swagger documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # ReDoc documentation
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]