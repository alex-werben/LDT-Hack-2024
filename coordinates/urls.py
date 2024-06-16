from django.urls import path
from .views import HouseListCreateView, StreetListView, ForecastListAPIView, PredictionListView, PriorityListAPIView, \
    HouseListView

urlpatterns = [
    path('houses/', HouseListCreateView.as_view(), name='house-list-create'),
    path('streets/', StreetListView.as_view(), name='street-list'),
    path('forecast/', ForecastListAPIView.as_view(), name='forecast'),
    path('predictions/', PredictionListView.as_view(), name='predictions-list'),
    # path('priority/<str:unoms>/', PriorityListAPIView.as_view(), name='unom-list'),
    path('priority/', PriorityListAPIView.as_view(), name='unom-list'),
    path('houses_list/<str:unom_list>/', HouseListView.as_view(), name='house-list'),
]
