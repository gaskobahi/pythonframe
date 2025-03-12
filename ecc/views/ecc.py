# myapp/views.py
from django.forms import FloatField
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from common.abilities.AbilityPermission import AbilityPermission
from common.authentification.CustomIsAuthenticated import CustomIsAuthenticated
from common.views.bases import BaseListCreateAPIView
from common.pagination import PaginationPersonnalise
from ecc.filters.ecc import EccFilter
from ecc.models.ecc import Ecc
from ecc.serializers.ecc import EccSerializer
from drf_yasg import openapi

from ecc.serializers.stock_movement import StockMovementSerializer
from ecc.services.stock_analysis_services import RemoveSpaces, aggregate_package_and_lot, filter_query_set, get_query_params

from django.db.models.functions import Round,Coalesce
from django.db.models import Sum, Case, When, Value, IntegerField,F,Avg,FloatField

from ecc.services.stock_analysis_services import TRANSACTION_TYPES, RemoveSpaces, filter_query_set, get_query_params
from django.db.models.functions import Cast


# Custom function to replace ',' with '.'

class EccListCreateView(APIView, BaseListCreateAPIView):
    serializer_class = EccSerializer
    filterset_class = EccFilter
    pagination_class = PaginationPersonnalise
    permission_classes = [CustomIsAuthenticated,AbilityPermission]
   
    @swagger_auto_schema(
        operation_description="Obtenir la liste des ECC",
        responses={
            200: EccSerializer(many=True),  # Retourne une liste d'objets
            400: openapi.Response("Bad Request"),  # Erreur de validation
            500: openapi.Response("Internal Server Error")
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

   