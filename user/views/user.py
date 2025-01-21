# myapp/views.py
from rest_framework.views import APIView

from common.pagination import PaginationPersonnalise
from common.views.bases import BaseDetailAPIView, BaseListCreateAPIView
from user.filters.user import UserFilter
from user.models.user import User
from user.serializers.user import UserSerializer


class UserListCreateView(APIView, BaseListCreateAPIView):
    serializer_class = UserSerializer
    filterset_class = UserFilter
    pagination_class = PaginationPersonnalise


class UserDetailView(APIView,BaseDetailAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'  # Utilise le champ `id` pour rechercher un produit
  
   
