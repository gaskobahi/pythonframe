# myapp/serializers.py

from product.serializers.category import CategorySerializer
from product.serializers.product import ProductSerializer



""" 
class OrderItemSerializer(AbstractBaseSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(AbstractBaseSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.customer_email = validated_data.get('customer_email', instance.customer_email)
        instance.save()

        keep_items = []
        for item_data in items_data:
            item_id = item_data.get('id')
            if item_id:
                item = OrderItem.objects.get(id=item_id, order=instance)
                item.product = item_data.get('product', item.product)
                item.quantity = item_data.get('quantity', item.quantity)
                item.save()
                keep_items.append(item.id)
            else:
                item = OrderItem.objects.create(order=instance, **item_data)
                keep_items.append(item.id)

        for item in instance.items.all():
            if item.id not in keep_items:
                item.delete()

        return instance
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

""" 