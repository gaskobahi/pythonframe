# myapp/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from common.views.bases import BaseDetailAPIView, BaseListCreateAPIView
from common.pagination import PaginationPersonnalise
from selling.filters.customer import CustomerFilter
from selling.models.customer import Customer
from selling.serializers.customer import CustomerSerializer


class CustomerListCreateView(APIView, BaseListCreateAPIView):
    #queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filterset_class = CustomerFilter
    pagination_class = PaginationPersonnalise


class CustomerDetailView(APIView,BaseDetailAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'pk'  # Utilise le champ `id` pour rechercher un produit
  
    @api_view(['POST'])
    def cancel(request, pk):
        try:
            Customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
        
        Customer.name = 'Canceled'
        Customer.save()
        return Response({'message': 'Customer canceled successfully'})
  
