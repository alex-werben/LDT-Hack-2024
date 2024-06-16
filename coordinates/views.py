import os
import pickle
import logging
import pandas as pd
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response
import json
from api_hack import settings
from .cool_down import cooling_time_for_unoms
from .filters import HouseFilter
from .models import House, DataModel
from .pagination import CustomLimitOffsetPagination
from .serializers import HouseSerializer, StreetSerializer, TempForecastSerializer, PredictionSerializer, \
    PrioritySerializer
from rest_framework import status
from rest_framework.views import APIView


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


class ForecastListAPIView(generics.ListAPIView):
    serializer_class = TempForecastSerializer

    def get(self, request, *args, **kwargs):
        ids = request.query_params.getlist('ids', [])
        ids = [int(id_) for id_ in ids if id_.isdigit()]

        if not ids:
            return Response({"detail": "No valid IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

        dt = request.query_params.get('dt', '2024-01-01 12:00')
        data = cooling_time_for_unoms(ids, dt)

        if data:
            serialized_data = [{"id": id_, **data[id_]} for id_ in data]
            return Response(serialized_data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No data found for provided IDs."}, status=status.HTTP_404_NOT_FOUND)


class PredictionListView(generics.ListAPIView):
    serializer_class = PredictionSerializer

    @staticmethod
    def get_file_list(directory):
        try:
            if os.path.exists(directory):
                file_list = os.listdir(directory)
                file_list = [f for f in file_list if os.path.isfile(os.path.join(directory, f))]
                return file_list
            else:
                print(f"Директория '{directory}' не существует.")
                return []
        except Exception as e:
            print(f"Ошибка при получении списка файлов: {str(e)}")
            return []

    def get_predict(self):
        unom = self.request.query_params.get('unom')
        instance = DataModel.objects.get(unom=unom)
        result_probability = {}
        df = pd.DataFrame({
            'district': [instance.district],
            'material': [instance.material],
            'purpose': [instance.purpose],
            'class': [instance.house_class],
            'event_cnt_cat': [instance.event_cnt_cat],
            'floor_num': [instance.floor_num],
            'flat_num': [instance.flat_num],
            'square': [instance.square]
        })
        pickle_files = self.get_file_list(os.path.join(settings.BASE_DIR, 'coordinates/pickle'))
        for pickle_file in pickle_files:
            with open(os.path.join(settings.BASE_DIR, f'coordinates/pickle/{pickle_file}'), 'rb') as file:
                model = pickle.load(file)
                predict = list(
                    model.predict_proba(df)[:, 1])
                result_probability[os.path.splitext(pickle_file)[0]] = predict
        return {
            'unom': unom,
            'probability': result_probability
        }

    def list(self, request, *args, **kwargs):
        queryset = [self.get_predict()]

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


# class PriorityListAPIView(generics.ListAPIView):
#     serializer_class = PrioritySerializer
#
#     @staticmethod
#     def get_priority(unom_list):
#         df = pd.read_csv(os.path.join(settings.BASE_DIR, r"data\merged_priority_data.csv"))
#         filtered_df = df[df['UNOM'].isin(unom_list)]
#         unom_type_dict = dict(zip(filtered_df['UNOM'], filtered_df['Тип Назначение']))
#         return [{'unom': k, 'priority': v} for k, v in unom_type_dict.items()]
#
#     def get_queryset(self):
#         unoms = self.kwargs['unoms']
#         try:
#             unom_list = json.loads(unoms)
#             if not isinstance(unom_list, list):
#                 raise ValueError
#         except (json.JSONDecodeError, ValueError):
#             return Response({'error': 'Invalid unom list format'}, status=status.HTTP_400_BAD_REQUEST)
#         print('unoms', unoms)
#         results = self.get_priority(unom_list)
#         return results
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         print('queryset', queryset)
#         if isinstance(queryset, Response):
#             return queryset
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

class PriorityListAPIView(APIView):
    serializer_class = PrioritySerializer

    @staticmethod
    def get_priority(unom_list):
        unom_list = [int(item) for item in unom_list]
        df = pd.read_csv(os.path.join(settings.BASE_DIR, r"data\merged_priority_data.csv"))
        filtered_df = df[df['UNOM'].isin(unom_list)]
        unom_type_dict = dict(zip(filtered_df['UNOM'], filtered_df['Тип Назначение']))
        return [{'unom': k, 'priority': v} for k, v in unom_type_dict.items()]

    def get(self, request, *args, **kwargs):
        unom_list = request.query_params.getlist('unom')
        if not unom_list:
            return Response({'error': 'No unom parameters provided'}, status=status.HTTP_400_BAD_REQUEST)
        results = self.get_priority(unom_list)
        serializer = self.serializer_class(results, many=True)
        return Response(serializer.data)


class HouseListView(generics.ListAPIView):
    serializer_class = HouseSerializer
    queryset = House.objects.all()

    def get_queryset(self):
        unom_list = self.kwargs.get('unom_list').split(',')
        return House.objects.filter(unom__in=unom_list)
