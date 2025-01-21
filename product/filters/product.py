import django_filters

from product.models.product import Product
from django.db.models import Q



class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category_name = django_filters.CharFilter(field_name="category__name", lookup_expr='exact')
    category_id = django_filters.CharFilter(field_name="category__id", lookup_expr='exact')
    name = django_filters.CharFilter(field_name="name", lookup_expr='iexact')
    search = django_filters.CharFilter(
        method='filter_search', 
        label='Recherche avancée'
    )

    def filter_search(self, queryset, name, value):
        # Appliquer une recherche flexible sur le nom de la catégorie et la description
        return queryset.filter(
            Q(category__name__icontains=value) | 
            Q(name__icontains=value)
        )

    class Meta:
        model = Product
        fields = ['name','category_id','category_name','min_price', 'max_price','search']

