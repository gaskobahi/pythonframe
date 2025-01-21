import django_filters

from selling.models.order import Order
from django.db.models import Q



class OrderFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    customer_name = django_filters.CharFilter(field_name="customer__name", lookup_expr='exact')
    product_name = django_filters.CharFilter(field_name="order_to_products__product__product__name", lookup_expr='exact')
    customer_id = django_filters.CharFilter(field_name="customer__id", lookup_expr='exact')

 
    def filter_search(self, queryset,name, value):
        return queryset.filter(
            Q(customer__first_name__icontains=value) |
            Q(customer__last_name__icontains=value) |
            Q(order_to_products__product__name__icontains=value) 
        )

    search = django_filters.CharFilter(
        method='filter_search', 
        label='Recherche avancée'
    )

   
    class Meta:
        model = Order
        fields = ['search']

