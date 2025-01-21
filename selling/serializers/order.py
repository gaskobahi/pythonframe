# myapp/serializers.py
from product.models.product import Product
from selling.models.customer import Customer
from selling.models.order import Order, OrderToProduct
from rest_framework import serializers

from base.serializers import AbstractBaseSerializer
from selling.serializers.customer import CustomerSerializer
from selling.serializers.orderToProduct import OrderToProductSerializer


class OrderSerializer(AbstractBaseSerializer):
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source="customer",
        allow_null=True,  # Allows the category to be null
        required=True    # Makes the field optional in the request
    )
      
    customer = CustomerSerializer(
        read_only=True,
        help_text="Objet Client",
        )
    order_to_products = OrderToProductSerializer(many=True) 
     # Allow multiple products
    class Meta:
        model = Order
        #fields = ['customer_id','order_to_products']
        #fields = '__all__'
        fields = ['id','customer_id','customer', 'order_to_products']
        read_only_fields = ['id']
   
    def create(self, validated_data):
        order_to_products_data = validated_data.pop('order_to_products',[])
        order = Order.objects.create(**validated_data)
        for product_data in order_to_products_data:
            OrderToProduct.objects.create(order=order, **product_data)
        return order 
   
    def update(self, instance, validated_data):
        product_id = instance.id
       # Traitement de la mise à jour de l'instance ici
        order_to_products_data = validated_data.pop('order_to_products', None)
        if order_to_products_data:
            for product_data in order_to_products_data:
                # Trouver ou mettre à jour les produits liés à la commande
                product = Product.objects.get(id=product_data['product_id'])
                # Appliquer d'autres modifications si nécessaire

        return super().update(instance, validated_data)