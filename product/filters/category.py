import django_filters

from product.models.category import Category
from django.db.models import Q



class CategoryFilter(django_filters.FilterSet):
    category_name = django_filters.CharFilter(field_name="category__name", lookup_expr='exact')
    name = django_filters.CharFilter(field_name="name", lookup_expr='iexact')
    # Exemple de filtrage avancé : filtrer par plusieurs critères combinés
    # Utilisation de Q objects pour des filtres complexes ou conditionnels
    search = django_filters.CharFilter(
        method='filter_search', 
        label='Recherche avancée'
    )

    def filter_search(self, queryset, name, value):
        # Appliquer une recherche flexible sur le nom de la catégorie et la description
        return queryset.filter(
            Q(name__icontains=value)
        )

    class Meta:
        model = Category
        fields = ['name']

