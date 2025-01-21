# myapp/models.py
from django.db import models # type: ignore

from base.models.base_core import BaseCoreEntity
from product.models.product import Product
from selling.models.customer import Customer

class Order(BaseCoreEntity):
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    #class Meta:
        #ordering = ['created_at']
    def __str__(self):
        return f"Order {self.id} by customer {self.customer.first_name}"

class OrderToProduct(BaseCoreEntity):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_to_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"