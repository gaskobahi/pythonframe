# myapp/serializers.py

from base.serializers import AbstractBaseSerializer
from ecc.models.ecc import Ecc

class EccSerializer(AbstractBaseSerializer):
    class Meta:
        model = Ecc
        fields = '__all__'
      