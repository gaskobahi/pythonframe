# myapp/views.py
from datetime import datetime

from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from common.abilities.AbilityPermission import AbilityPermission
from common.authentification.CustomIsAuthenticated import CustomIsAuthenticated
from ecc.serializers.ecc import EccSerializer
from ecc.serializers.stock_movement import StockMovementSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from ecc.services.stock_analysis_services import get_mvt_by_package_lot_number_service, get_mvt_by_variant_code_service, get_stockmovement_service


# Custom function to replace ',' with '.'


current_year = datetime.now().year  # Récupère l'année en entier (ex: 2024)
previous_year=current_year-1

class StockMovementView(APIView):#BaseListCreateAPIView
    serializer_class = EccSerializer
    permission_classes = [CustomIsAuthenticated,AbilityPermission]

    # 🔹 Route 1 : Analyse des mouvements de stock
    @swagger_auto_schema(
        method='get',
        operation_description="Analyse des mouvements de stock avec filtres",
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Début de l'analyse", type=openapi.TYPE_STRING),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="Fin de l'analyse", type=openapi.TYPE_STRING),
            openapi.Parameter('article_number', openapi.IN_QUERY, description="Numéro d'article", type=openapi.TYPE_STRING),
            openapi.Parameter('variant_code', openapi.IN_QUERY, description="Code variant", type=openapi.TYPE_STRING),
            openapi.Parameter('type_ecriture', openapi.IN_QUERY, description="Type d'écriture", type=openapi.TYPE_STRING),
        ],
        responses={200: StockMovementSerializer(many=True)}
    )
    @api_view(['get'])
    def get_stockmovement(request):
        result=get_stockmovement_service(request)
        serializer = StockMovementSerializer(result, many=True)
        return Response(serializer.data)

    # 🔹 Route 2 : Analyse des stocks par numéro de package/lot
    @swagger_auto_schema(
        method='get',
        operation_description="Analyse des stocks par numéro de package/lot",
        manual_parameters=[
            openapi.Parameter('package_lot', openapi.IN_QUERY, description="Numéro de package/lot", type=openapi.TYPE_STRING),
        ],
        responses={200: StockMovementSerializer(many=True)}
    )

    @api_view(['get'])
    def get_mvt_by_package_lot_number(request, *args, **kwargs):
        result=get_mvt_by_package_lot_number_service(request)
        # Sérialisation et réponse
        serializer = StockMovementSerializer(result, many=True)
        return Response(serializer.data,status=200)
    

     # 🔹 Route 2 : Analyse des stocks par numéro de package/lot

    @swagger_auto_schema(
        method='get',
        operation_description="Analyse des stocks par code variant",
        manual_parameters=[
            openapi.Parameter('varant_code', openapi.IN_QUERY, description="Code Variant", type=openapi.TYPE_STRING),
        ],
        responses={200: StockMovementSerializer(many=True)}
    )
    @api_view(['get'])
    def get_mvt_by_variant_code(request):
        #params = get_query_params(request)
        result_service=get_mvt_by_variant_code_service(request)
        # Sérialisation et réponse
        serializer = StockMovementSerializer(result_service, many=True)
        return Response(serializer.data)
