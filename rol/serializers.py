from .models import Rol
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer



class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'url', 'nombre', 'descripcion', 'habilitado', 'created_at']
