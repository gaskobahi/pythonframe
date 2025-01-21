# myapp/serializers.py
from rest_framework import serializers

from base.serializers import AbstractBaseSerializer
from product.serializers.category import CategorySerializer
from product.models.category import Category
from product.models.product import Product


class ProductSerializer(AbstractBaseSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        allow_null=True,  # Allows the category to be null
        required=True    # Makes the field optional in the request
    )
    category = CategorySerializer(read_only=True)  # Sérialiseur imbriqué pour la catégorie

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id']

