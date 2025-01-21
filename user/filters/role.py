import django_filters

from django.db.models import Q

from user.models.role import Role



class RoleFilter(django_filters.FilterSet):
    role_name = django_filters.CharFilter(field_name="role__name", lookup_expr='exact')
    name = django_filters.CharFilter(field_name="name", lookup_expr='iexact')

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
        model = Role
        fields = ['name']

