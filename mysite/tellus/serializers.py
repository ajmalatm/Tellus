from .models import *
from rest_framework import serializers

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model=Formsix
        fields=['id','bldg_stats','bldg_usage','bldg_zone','centrl_ac','year_const','ward_nm','geom']

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Owner_Details
        fields='__all__'

