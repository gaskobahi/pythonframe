from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from base.enums import AbilityActionEnum

class BaseListCreateAPIView:
    """
    Classe abstraite pour gérer les opérations de liste et de création
    avec pagination et filtres.
    """
    queryset = None
    serializer_class = None
    filterset_class = None
    pagination_class = PageNumberPagination

    
    resource_action_map = {
        "GET": AbilityActionEnum.read,  # Maps HTTP methods to actions
        "POST": AbilityActionEnum.create
    }

    @property
    def resource_subject(self):
        """
        Retrieve the resource name dynamically based on the serializer class.
        """
        if self.serializer_class and hasattr(self.serializer_class.Meta, "model"):
            # Use the model's name if defined in the serializer's Meta class
            return self.serializer_class.Meta.model.__name__
        elif self.serializer_class:
            # Fallback: Use the serializer class name
            return self.serializer_class.__name__.replace("Serializer", "")
        return None  # Default fallback if no serializer is defined

    def get_resource_action(self):
        # Gracefully handle cases where request or method might not exist
        if not hasattr(self, 'request') or not getattr(self.request, 'method', None):
            return None
        return self.resource_action_map.get(self.request.method, None)

    def get_queryset(self):
        """
        Retourne le queryset à utiliser pour cette vue.
        Peut être personnalisé par les sous-classes.
        """
        return self.queryset

    def apply_filters(self, request):
        """
        Applique les filtres au queryset en utilisant la `filterset_class`.
        """
        queryset = self.get_queryset()
        if self.filterset_class:
            filterset = self.filterset_class(data=request.GET, queryset=queryset, request=request)
            if filterset.is_valid():
                return filterset.qs
        return queryset

    def paginate_queryset(self, queryset, request):
        """
        Paginate the queryset using the defined pagination class.
        """
        paginator = self.pagination_class()
        return paginator.paginate_queryset(queryset, request), paginator

    @swagger_auto_schema(
        operation_summary="Liste de x",
        operation_description="Récupère une liste",
        responses={200: serializer_class},
    )
    def get(self, request, *args, **kwargs):
        """
        Gestion des requêtes GET avec filtres et pagination.
        """
        queryset = self.apply_filters(request)
        paginated_queryset, paginator = self.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Créer ",
        operation_description="Permet de créer avec un corps de requête valide.",
        request_body=serializer_class,  # Associer le sérialiseur ici
        responses={
            201: openapi.Response("créé avec succès", serializer_class),
            400: "Données invalides",
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Gestion des requêtes POST pour créer un nouvel objet.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "POST endpoint","data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class BaseDetailAPIView:
    """
    Classe abstraite pour gérer les opérations CRUD sur un objet unique.
    """
    queryset = None
    serializer_class = None
    lookup_field = 'pk'  # Par défaut, utilise la clé primaire
    resource_action_map = {
        "GET": AbilityActionEnum.read,  # Maps HTTP methods to actions
        "POST":AbilityActionEnum.create,
        "PATCH":AbilityActionEnum.edit,
        "PUT":AbilityActionEnum.edit,
        "DELETE":AbilityActionEnum.delete
    }

    @property
    def resource_subject(self):
        """
        Retrieve the resource name dynamically based on the serializer class.
        """
        if self.serializer_class and hasattr(self.serializer_class.Meta, "model"):
            # Use the model's name if defined in the serializer's Meta class
            return self.serializer_class.Meta.model.__name__
        elif self.serializer_class:
            # Fallback: Use the serializer class name
            return self.serializer_class.__name__.replace("Serializer", "")
        return None  # Default fallback if no serializer is defined
    
    def get_resource_action(self):
        return self.resource_action_map.get(self.request.method, None)

    def get_queryset(self):
        """
        Retourne le queryset ou lève une exception si absent.
        """
        if self.queryset is None:
            raise ValueError("Vous devez définir un queryset dans la sous-classe.")
        return self.queryset


    def get_object(self, lookup_value):
        """
        Retourne l'objet correspondant à la requête ou lève une erreur 404.
        """
        return get_object_or_404(self.queryset, **{self.lookup_field: lookup_value})

    def get(self, request, *args, **kwargs):
        print("test",self)

        """
        Gère les requêtes GET pour récupérer un objet.
        """
        obj = self.get_object(kwargs.get(self.lookup_field))
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        """
        Gère les requêtes PUT pour mettre à jour un objet entier.
        """
        obj = self.get_object(kwargs.get(self.lookup_field))
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        """
        Gère les requêtes PATCH pour une mise à jour partielle.
        """
        obj = self.get_object(kwargs.get(self.lookup_field))
        serializer = self.serializer_class(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Gère les requêtes DELETE pour supprimer un objet.
        """
        obj = self.get_object(kwargs.get(self.lookup_field))
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



