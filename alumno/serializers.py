from rest_framework import serializers
from .models import Alumno
from carrera.serializers import CarreraSerializer
from materia.serializers import MateriaSerializer
from drf_writable_nested import WritableNestedModelSerializer


class AlumnoSerializer(WritableNestedModelSerializer, serializers.HyperlinkedModelSerializer):
    carreras = CarreraSerializer()
    materias = MateriaSerializer()

    class Meta:
        model = Alumno
        fields = [
                    'id', 'url', 'nombre', 'apellido', 'dni', 'correo', 'direccion',
                    'telefono', 'materias', 'carreras', 'habilitado', 'created_at'
                ]
