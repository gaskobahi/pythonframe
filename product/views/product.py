# myapp/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from common.pagination import PaginationPersonnalise
from common.views.bases import BaseDetailAPIView, BaseListCreateAPIView
from product.models.product import Product
from product.filters.product import ProductFilter
from product.serializers.product import ProductSerializer

class ProductListCreateView(APIView,BaseListCreateAPIView):
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    pagination_class = PaginationPersonnalise


class ProductDetailView(APIView,BaseDetailAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'  # Utilise le champ `id` pour rechercher un produit
    
    @api_view(['POST'])
    def cancel(request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        product.name = 'Canceled'
        product.save()
        return Response({'message': 'product canceled successfully'})


