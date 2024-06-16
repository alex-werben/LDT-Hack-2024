from rest_framework import serializers
from .models import House


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'


class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ['street']

    def to_representation(self, instance):
        return instance['street']


class TempForecastSerializer(serializers.Serializer):
    temp_forecast = serializers.ListField()
    cooling_down_till_standard_h = serializers.IntegerField()
    full_cooling_down = serializers.CharField()


class PredictionSerializer(serializers.Serializer):
    unom = serializers.CharField()
    probability = serializers.DictField(child=serializers.ListField(child=serializers.FloatField()))


class PrioritySerializer(serializers.Serializer):
    unom = serializers.IntegerField()
    priority = serializers.IntegerField()
