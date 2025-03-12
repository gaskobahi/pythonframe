# myapp/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from common.views.bases import BaseDetailAPIView, BaseListCreateAPIView
from common.pagination import PaginationPersonnalise
from ecc.filters.temp_ecc import TempEccFilter
from ecc.models.temp_ecc import Temp_Ecc
from ecc.serializers.temp_ecc import TempEccSerializer



class TempEccListCreateView(APIView, BaseListCreateAPIView):
    serializer_class = TempEccSerializer
    filterset_class = TempEccFilter
    pagination_class = PaginationPersonnalise


class TempEccDetailView(APIView,BaseDetailAPIView):
    queryset = Temp_Ecc.objects.all()
    serializer_class = TempEccSerializer
    lookup_field = 'pk'  # Utilise le champ `id` pour rechercher un produit
  
    @api_view(['POST'])
    def cancel(request, pk):
        try:
            TempEcc = TempEcc.objects.get(pk=pk)
        except TempEcc.DoesNotExist:
            return Response({'error': 'TempEcc not found'}, status=status.HTTP_404_NOT_FOUND)
        
        TempEcc.name = 'Canceled'
        TempEcc.save()
        return Response({'message': 'TempEcc canceled successfully'})
