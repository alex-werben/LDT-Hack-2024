from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .filters import HouseFilter
from .models import House
from .pagination import CustomLimitOffsetPagination
from .serializers import HouseSerializer, StreetSerializer


class HouseListCreateView(generics.ListAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HouseFilter
    pagination_class = CustomLimitOffsetPagination

    def get_queryset(self):
        queryset = self.queryset
        queryset = self.filterset_class(self.request.GET, queryset=queryset).qs
        return queryset


class StreetListView(generics.ListAPIView):
    serializer_class = StreetSerializer

    def get_queryset(self):
        # Извлекаем уникальные улицы (поля 'street') из модели House
        queryset = House.objects.values('street').distinct()
        return queryset
