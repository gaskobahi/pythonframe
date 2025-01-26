# myapp/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from common.abilities.AbilityPermission import AbilityPermission
from common.authentification.CustomIsAuthenticated import CustomIsAuthenticated
from common.pagination import PaginationPersonnalise
from common.views.bases import BaseDetailAPIView, BaseListCreateAPIView
from product.filters.category import CategoryFilter
from product.models.category import Category
from product.serializers.category import CategorySerializer

class CategoryListCreateView(APIView, BaseListCreateAPIView):
    permission_classes = [CustomIsAuthenticated,AbilityPermission]
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter
    pagination_class = PaginationPersonnalise
 # Define the resource and action
    #resource_subject = "User"  # The name of the resource (subject)
    

class CategoryDetailView(APIView,BaseDetailAPIView):
    permission_classes = [CustomIsAuthenticated,AbilityPermission]
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
  
