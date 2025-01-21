# myapp/serializers.py

from base.serializers import AbstractBaseSerializer
from selling.models.customer import Customer

class CustomerSerializer(AbstractBaseSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
      