# myapp/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from common.pagination import PaginationPersonnalise
from common.views.bases import BaseDetailAPIView, BaseListCreateAPIView
from product.filters.category import CategoryFilter
from product.models.category import Category
from product.serializers.category import CategorySerializer


class CategoryListCreateView(APIView, BaseListCreateAPIView):
    #queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter
    pagination_class = PaginationPersonnalise


class CategoryDetailView(APIView,BaseDetailAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'  # Utilise le champ `id` pour rechercher un produit
  
    @api_view(['POST'])
    def cancel(request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        
        category.name = 'Canceled'
        category.save()
        return Response({'message': 'Category canceled successfully'})
  
