# from rest_framework import serializers
# from .models import Asistencia
# from carrera.serializers import CarreraSerializer
# from materia.serializers import MateriaSerializer
# from alumno.serializers import AlumnoSerializer
# from drf_writable_nested import WritableNestedModelSerializer


# class AsistenciaSerializer(WritableNestedModelSerializer, serializers.HyperlinkedModelSerializer):
#     carrera = CarreraSerializer
#     materia = MateriaSerializer
#     alumnos = AlumnoSerializer(many=True)
#     estado = serializers.StringRelatedField(source='asistenciaalumno_set.first.estado')
#     class Meta:
#         model = Asistencia
#         fields = [
#                     'id', 'url', 'fecha', 'carrera', 'materia', 'alumnos', 'estado', 'habilitado', 'created_at'
#                 ]
        
from carrera.serializers import CarreraSerializer
from materia.serializers import MateriaSerializer
from alumno.serializers import AlumnoSerializer
from rest_framework import serializers
from .models import Asistencia, AsistenciaAlumno
from estado_asistencia.serializers import EstadoAsistenciaSerializer
from drf_writable_nested import WritableNestedModelSerializer

class AsistenciaSerializer(serializers.ModelSerializer):
    carrera = CarreraSerializer()
    materia = MateriaSerializer()
    alumnos = AlumnoSerializer(many=True)
    # estado_alumnos = serializers.SerializerMethodField()
    
    class Meta:
        model = Asistencia
        fields = [
            'id', 'url', 'fecha', 'carrera', 'materia', 'alumnos', 'cantidad_presentes','cantidad_ausentes','cantidad_tardanza','cantidad_justificados','habilitado', 'created_at', 
        ]

    def get_estado_alumnos(self, obj):
        estado_alumnos = {}
        for asistencia_alumno in obj.asistenciaalumno_set.all():
            estado_alumnos[asistencia_alumno.alumno.id] = asistencia_alumno.estado.nombre
        return estado_alumnos
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        estado_alumnos = self.get_estado_alumnos(instance)
        for alumno_data in representation['alumnos']:
            alumno_id = alumno_data['id']
            alumno_data['estado_asistencia'] = estado_alumnos.get(alumno_id)
           
        return representation