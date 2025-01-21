# myapp/serializers.py

from base.serializers import AbstractBaseSerializer
from user.models.role import Role

class RoleSerializer(AbstractBaseSerializer):
    class Meta:
        model = Role
        fields = '__all__'
      