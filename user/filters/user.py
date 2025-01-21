import django_filters

from django.db.models import Q

from user.models.user import User




class UserFilter(django_filters.FilterSet):
    role_name = django_filters.CharFilter(field_name="role__name", lookup_expr='exact')
    role_id = django_filters.CharFilter(field_name="role__id", lookup_expr='exact')
    name = django_filters.CharFilter(field_name="name", lookup_expr='iexact')
    search = django_filters.CharFilter(
        method='filter_search', 
        label='Recherche avancée'
    )

    def filter_search(self, queryset, name, value):
        # Appliquer une recherche flexible sur le nom de la catégorie et la description
        return queryset.filter(
            Q(role__name__icontains=value) | 
            Q(name__icontains=value)
        )

    class Meta:
        model = User
        fields = ['name','role_id','role_name','search']

