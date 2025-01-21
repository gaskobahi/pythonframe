from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import update_last_login
from rest_framework import status

from common.authentification.CustomIsAuthenticated import CustomIsAuthenticated
from custom_auth.serializers.change_password_serializers import ChangePasswordSerializer
from custom_auth.services.auth_service import AuthService


class ChangePasswordView(APIView):
    permission_classes = [CustomIsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        authService=AuthService(request)
        user = request.user

        #return change_password.change_password(serializer.validated_data);
        # Check if current password matches
        if not user.check_password(serializer.validated_data['current_password']):
            raise ValidationError({'current_password': ['Mot de passe actuel incorrect']})

        # Update the password
        user.set_password(serializer.validated_data['password'])
        user.save()

        # logout current user logged
        authService.logout()
        return Response({'message': 'Mot de passe mis à jour avec succès.'},status=status.HTTP_205_RESET_CONTENT)
