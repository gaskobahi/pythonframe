# myapp/serializers.py
from rest_framework import serializers
from product.models.product import Product
from product.serializers.product import ProductSerializer
from selling.models.order import OrderToProduct
from base.serializers import AbstractBaseSerializer


class OrderToProductSerializer(AbstractBaseSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
            queryset=Product.objects.all(),
            source="product",
            allow_null=True,  # Allows the category to be null
            required=True,    # Makes the field optional in the request
        ) 
       
    #product_id = serializers.UUIDField(write_only=True)  # Pour accepter uniquement des UUIDs
    product = ProductSerializer(read_only=True)
    quantity = serializers.IntegerField()
    price = serializers.IntegerField()

    class Meta:
        model = OrderToProduct
        #fields = '__all__'
        fields = ('product','product_id','quantity', 'price')
        read_only_fields = ['id']

