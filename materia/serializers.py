from rest_framework import serializers
from .models import Materia
from modulo.serializers import ModuloSerializer
from carrera.serializers import CarreraSerializer
from drf_writable_nested import WritableNestedModelSerializer


class MateriaSerializer(WritableNestedModelSerializer, serializers.HyperlinkedModelSerializer):
    carrera = CarreraSerializer()
    modulos = ModuloSerializer()

    class Meta:
        model = Materia
        fields = ['id', 'url', 'nombre', 'descripcion', 'anual', 'carrera', 'modulos',
                   'habilitado', 'created_at']
