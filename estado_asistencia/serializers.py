from .models import EstadoAsistencia
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer



class EstadoAsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoAsistencia
        fields = ['id', 'url', 'nombre', 'descripcion', 'habilitado', 'created_at']
