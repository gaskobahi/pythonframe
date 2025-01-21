# myapp/serializers.py

from base.serializers import AbstractBaseSerializer
from product.models.category import Category
from rest_framework import serializers

class CategorySerializer(AbstractBaseSerializer):
    class Meta:
        model = Category
        fields = '__all__'
      