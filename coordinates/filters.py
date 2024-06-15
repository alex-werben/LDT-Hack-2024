import django_filters
from .models import House


class HouseFilter(django_filters.FilterSet):
    street = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = House
        fields = ['street']
