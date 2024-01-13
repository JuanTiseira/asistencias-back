from .models import Asistencia
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import AsistenciaSerializer
from rest_framework.authentication import TokenAuthentication
from api.permissions import CustomDjangoModelPermissions 
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdminOrReadOnly
from rest_framework.response import Response

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer()
    # permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        queryset = Asistencia.objects.all()
        fecha = self.request.query_params.get('fecha')
        carrera = self.request.query_params.get('carrera')
        materia = self.request.query_params.get('materia')
        alumnos = self.request.query_params.get('alumnos')
        habilitado = self.request.query_params.get('habilitado')

        if habilitado is not None:
            queryset = queryset.filter(habilitado=habilitado)
        else:
            queryset = queryset.filter(habilitado=True)

        if fecha is not None:
            queryset = queryset.filter(fecha=fecha)
        if carrera is not None:
            queryset = queryset.filter(carrera=carrera)
        if materia is not None:
            queryset = queryset.filter(materia=materia)
        if carrera is not None:
            alumnos = queryset.filter(alumnos=alumnos)
        return queryset
