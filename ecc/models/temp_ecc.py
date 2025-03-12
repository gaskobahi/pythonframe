# myapp/models.py

from base.models.base_ecc import BaseEccEntity
from django.db import models

class Temp_Ecc(BaseEccEntity):
      sequence_number = models.BigIntegerField(primary_key=True)  # Clé primaire personnalisée