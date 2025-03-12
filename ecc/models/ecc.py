# myapp/models.py
from base.models.base_ecc import BaseEccEntity
from django.db import models

class Ecc(BaseEccEntity):
    id = models.CharField(max_length=255, primary_key=True)  # Explicitly set as primary key


    """#def __str__(self):
    #return self.id
    """