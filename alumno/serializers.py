from rest_framework import serializers
from .models import Alumno
from carrera.serializers import CarreraSerializer
from materia.serializers import MateriaSerializer
from drf_writable_nested import WritableNestedModelSerializer


class AlumnoSerializer(WritableNestedModelSerializer, serializers.HyperlinkedModelSerializer):
    carreras = CarreraSerializer(many=True)

    class Meta:
        model = Alumno
        fields = [
                    'id', 'url', 'nombre', 'apellido', 'dni', 'email', 'direccion',
                    'telefono', 'carreras', 'habilitado', 'fecha_nacimiento', 'created_at'
                ]
