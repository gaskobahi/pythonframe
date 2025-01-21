# myapp/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from common.pagination import PaginationPersonnalise
from common.views.bases import BaseDetailAPIView, BaseListCreateAPIView
from selling.filters.order import OrderFilter
from selling.models.order import Order
from selling.serializers.order import OrderSerializer

class OrderListCreateView(APIView,BaseListCreateAPIView):
    serializer_class = OrderSerializer
    filterset_class = OrderFilter
    pagination_class = PaginationPersonnalise


class OrderDetailView(APIView,BaseDetailAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'  # Utilise le champ `id` pour rechercher un produit
    
    @api_view(['POST'])
    def cancel(request, pk):
        try:
            selling = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'selling not found'}, status=status.HTTP_404_NOT_FOUND)
        selling.name = 'Canceled'
        selling.save()
        return Response({'message': 'selling canceled successfully'})


