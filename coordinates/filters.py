import django_filters
from .models import House
from django.db.models import Q


class HouseFilter(django_filters.FilterSet):
    street = django_filters.CharFilter(lookup_expr='icontains')
    municipal_district = django_filters.CharFilter(lookup_expr='icontains')
    unom_houses = django_filters.CharFilter(method='filter_unom_houses')

    def filter_unom_houses(self, queryset, name, value):
        # Исключаем строки, где unom_houses равно "nan"
        return queryset.exclude(Q(unom_houses="nan") | Q(unom_houses__isnull=True))

    class Meta:
        model = House
        fields = ['street', 'municipal_district', 'unom_houses']
