# myapp/serializers.py

from base.serializers import AbstractBaseSerializer
from ecc.models.temp_ecc import Temp_Ecc

class TempEccSerializer(AbstractBaseSerializer):
    class Meta:
        model = Temp_Ecc
        fields = '__all__'
      