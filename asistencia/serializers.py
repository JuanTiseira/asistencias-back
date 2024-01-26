from rest_framework import serializers
from .models import Asistencia
from carrera.serializers import CarreraSerializer
from materia.serializers import MateriaSerializer
from alumno.serializers import AlumnoSerializer
from drf_writable_nested import WritableNestedModelSerializer


class AsistenciaSerializer(WritableNestedModelSerializer, serializers.HyperlinkedModelSerializer):
    carrera = CarreraSerializer()
    materia = MateriaSerializer()
    alumnos = AlumnoSerializer()

    class Meta:
        model = Asistencia
        fields = [
                    'id', 'url', 'fecha', 'carrera', 'materia', 'alumnos', 'habilitado', 'created_at'
                ]
        