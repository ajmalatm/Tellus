from .models import *
from rest_framework import serializers

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Layergroup
        fields='__all__'

class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Layer
        fields='__all__'


class BasemapSerializer(serializers.ModelSerializer):
    class Meta:
        model=Basemap
        fields='__all__'

class MapConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Map_Config
        fields='__all__'