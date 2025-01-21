# myapp/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.pagination import PaginationPersonnalise
from common.views.bases import BaseDetailAPIView, BaseListCreateAPIView
from user.filters.role import RoleFilter
from user.models.role import Role
from user.serializers.role import RoleSerializer


class RoleListCreateView(APIView, BaseListCreateAPIView):
    serializer_class = RoleSerializer
    filterset_class = RoleFilter
    pagination_class = PaginationPersonnalise


class RoleDetailView(APIView,BaseDetailAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_field = 'pk'  # Utilise le champ `id` pour rechercher un produit
  
   
