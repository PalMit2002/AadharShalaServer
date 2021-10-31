from . import models
from rest_framework import serializers


class LandlordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Landlord
        fields = '__all__'


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tenant
        fields = ['reqCode']
