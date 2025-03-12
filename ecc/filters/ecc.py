import django_filters
from django.db.models import Q
from ecc.models.ecc import Ecc


class EccFilter(django_filters.FilterSet):
    #ecc_name = django_filters.CharFilter(field_name="ecc__name", lookup_expr='exact')
    #name = django_filters.CharFilter(field_name="name", lookup_expr='iexact')
    # Exemple de filtrage avancé : filtrer par plusieurs critères combinés
    # Utilisation de Q objects pour des filtres complexes ou conditionnels
    search = django_filters.CharFilter(
        method='filter_search', 
        label='Recherche avancée'
    )

    def filter_search(self, queryset, sequence_number, value):
        # Appliquer une recherche flexible sur le nom de la catégorie et la description
        return queryset.filter(
            Q(sequence_number__icontains=value)
        )

    class Meta:
        model = Ecc
        fields = ['sequence_number']

