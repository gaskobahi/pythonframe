# myapp/models.py
from django.db import models

from base.models.base_core import BaseCoreEntity
from product.models.category import Category

class Product(BaseCoreEntity):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE ,blank=True)

    def is_expensive(self):
        return self.price > 500  # Example method
    
    def __str__(self):
        return f"Products for {self.category.name} with {self.name} on {self.price}"
    