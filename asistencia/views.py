from .models import Asistencia, AsistenciaAlumno
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import AsistenciaSerializer
from rest_framework.authentication import TokenAuthentication
from api.permissions import CustomDjangoModelPermissions
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdminOrReadOnly
from rest_framework.response import Response
from django.db.models import Prefetch
from django.http import JsonResponse
from django.core.serializers import serialize
from rest_framework.decorators import action
from rest_framework import viewsets, status

from carrera.models import Carrera
from alumno.models import Alumno
from materia.models import Materia
from estado_asistencia.models import EstadoAsistencia

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.prefetch_related(
        Prefetch('asistenciaalumno_set', queryset=AsistenciaAlumno.objects.select_related('estado'), to_attr='asistencias_alumnos')
    )

    serializer_class = AsistenciaSerializer
    # permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        queryset = super().get_queryset()
        fecha = self.request.query_params.get('fecha')
        carrera = self.request.query_params.get('carrera')
        materia = self.request.query_params.get('materia')
        alumnos = self.request.query_params.get('alumno')
        habilitado = self.request.query_params.get('habilitado')

        if habilitado is not None:
            queryset = queryset.filter(habilitado=habilitado)
        else:
            queryset = queryset.filter(habilitado=True)

        if fecha is not None:
            queryset = queryset.filter(fecha=fecha)
        if carrera is not None:
            queryset = queryset.filter(carrera_id=carrera)
        if materia is not None:
            queryset = queryset.filter(materia=materia)
        if alumnos is not None:
            queryset = queryset.filter(asistenciaalumno__alumno_id=alumnos)

        print(alumnos,queryset)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Verificar si el queryset está vacío
        if not queryset.exists():
            # Personaliza la respuesta si el queryset está vacío
            return Response(
                {'message': 'No se encontraron resultados para la solicitud.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def view_asistencia(self, request):
        print("holaasas")
        if request.method == 'GET':
            # asistencias = Asistencia.objects.all()
            asistencias = AsistenciaAlumno.objects.all()
            print(asistencias)
            asistencias = AsistenciaSerializer(asistencias, many=True, context={'request': request}).data
            return Response(data={'success': True, 'message': "Usuario modificado.", "data" : asistencias},
                        status= status.HTTP_201_CREATED)
        else:
            return JsonResponse({'error': 'Método no permitido'}, status=405)



    def create(self, request, *args, **kwargs):
        try:
            # Obtener datos del JSON
            fecha = request.data.get('fecha')
            carrera = request.data.get('carrera')
            materia = request.data.get('materia')
            alumnos_estado_asistencia = request.data.get('alumnos_estado_asistencia')  # Lista de diccionarios con id del alumno y estado de asistencia
            # print("llegeu", carrera.get("id"), materia.get("id"))
            # Obtener carrera y materia
            carrera = Carrera.objects.get(id=carrera.get("id"))
            materia = Materia.objects.get(id=materia.get("id"))
            print(carrera.id, materia.id)
            # # Crear la asistencia
            # asistencia = Asistencia.objects.create(fecha=fecha, carrera=carrera, materia=materia)

            # # Recorrer la lista de alumnos y sus estados de asistencia
            # for alumno_estado in alumnos_estado_asistencia:
            #     alumno_id = alumno_estado.get('alumno_id')
            #     estado_asistencia_id = alumno_estado.get('estado_asistencia_id')

            #     # Obtener el alumno y el estado de asistencia
            #     alumno = Alumno.objects.get(id=alumno_id)
            #     estado_asistencia = EstadoAsistencia.objects.get(id=estado_asistencia_id)

            #     # Crear la relación entre la asistencia y el alumno con su estado de asistencia
            #     AsistenciaAlumno.objects.create(asistencia=asistencia, alumno=alumno, estado=estado_asistencia)

            return Response(data={'success': True, 'message': "Asistencia registrada correctamente."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(data={'success': False, 'message': "Error al registrar la asistencia.", 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
