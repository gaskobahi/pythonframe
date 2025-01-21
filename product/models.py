# myapp/models.py
from product.models.category  import Category
from product.models.product  import Product



"""
class Category(BaseCoreEntity):
    name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name

class Product(BaseCoreEntity):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE ,blank=True)

    def is_expensive(self):
        return self.price > 500  # Example method
    def __str__(self):
        return f"Products for {self.category.name} with {self.name} on {self.price}"
    

class Order(BaseCoreEntity):
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()

    def __str__(self):
        return f"Order {self.id} by {self.customer_name}"

class OrderItem(BaseCoreEntity):

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
"""