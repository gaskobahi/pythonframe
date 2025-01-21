# myapp/serializers.py
from datetime import datetime
import uuid
from rest_framework import serializers

from base.serializers import AbstractBaseSerializer
from user.models.user import User
from user.models.role import Role
from user.serializers.role import RoleSerializer

def custom_serializer(obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")



class UserSerializer(AbstractBaseSerializer):
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        source="role",
        allow_null=True,  # Allows the category to be null
        required=True    # Makes the field optional in the request
    )
    role = RoleSerializer(read_only=True)  # Sérialiseur imbriqué pour la catégorie

    class Meta:
        model = User
        fields = '__all__'
        #read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        """
        Customize serialization to handle UUID and other complex types.
        """
        representation = super().to_representation(instance)
        # Convert UUID to string
        representation["id"] = str(instance.id)
        return representation
    
   