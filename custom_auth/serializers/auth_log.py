# myapp/serializers.py

from base.serializers import AbstractBaseSerializer
from user.models.auth_log import AuthLog


class AuthLogSerializer(AbstractBaseSerializer):

    class Meta:
        model = AuthLog
        fields = '__all__'
        read_only_fields = ['id']

