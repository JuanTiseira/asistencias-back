from .models import Carrera
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer



class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrera
        fields = ['id', 'url', 'nombre', 'descripcion', 'habilitado', 'created_at']
