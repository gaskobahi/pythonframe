# myapp/serializers.py

from base.serializers import AbstractBaseSerializer
from product.models.category import Category

class CategorySerializer(AbstractBaseSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id']
