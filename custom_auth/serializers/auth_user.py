# myapp/serializers.py
from rest_framework import serializers

from base.serializers import AbstractBaseSerializer
from custom_auth.models.auth_user import AuthUser
from user.models.role import Role
from user.models.user import User
from user.serializers.role import RoleSerializer
from user.serializers.user import UserSerializer


class AuthUserSerializer(AbstractBaseSerializer):
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        source="role",
        allow_null=True,  # Allows the category to be null
        required=True    # Makes the field optional in the request
    )
    role = RoleSerializer(read_only=True)  # Sérialiseur imbriqué pour la catégorie
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="user",
        allow_null=True,  # Allows the category to be null
        required=True    # Makes the field optional in the request
    )
    user = UserSerializer(read_only=True)  # Sérialiseur imbriqué pour la catégorie

    class Meta:
        model = AuthUser
        fields = '__all__'
        read_only_fields = ['id']

