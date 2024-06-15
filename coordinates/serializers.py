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
