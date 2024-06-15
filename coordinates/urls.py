from django.urls import path
from .views import HouseListCreateView, StreetListView

urlpatterns = [
    path('houses/', HouseListCreateView.as_view(), name='house-list-create'),
    path('streets/', StreetListView.as_view(), name='street-list'),
]
