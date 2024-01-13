from .models import Modulo
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer



class ModuloSerializer(serializers.ModelSerializer):

    class Meta:
        model = Modulo
        fields = ['id', 'url', 'nombre', 'descripcion', 'habilitado', 'created_at']
