from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

class AbstractBaseView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.all()

    def get_serializer_class(self):
        return self.serializer_class
