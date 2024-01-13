from .models import Alumno
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import AlumnoSerializer
from rest_framework.authentication import TokenAuthentication
from api.permissions import CustomDjangoModelPermissions 
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdminOrReadOnly
from rest_framework.response import Response

class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer()
    # permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        queryset = Alumno.objects.all()
        nombre = self.request.query_params.get('nombre')
        apellido = self.request.query_params.get('apellido')
        dni = self.request.query_params.get('dni')
        carrera = self.request.query_params.get('carrera')
        materia = self.request.query_params.get('materia')
        habilitado = self.request.query_params.get('habilitado')

        if habilitado is not None:
            queryset = queryset.filter(habilitado=habilitado)
        else:
            queryset = queryset.filter(habilitado=True)

        if nombre is not None:
            queryset = queryset.filter(nombre=nombre)
        if apellido is not None:
            queryset = queryset.filter(apellido=apellido)
        if dni is not None:
            queryset = queryset.filter(dni=dni)
        if carrera is not None:
            queryset = queryset.filter(carreras=carrera)
        if materia is not None:
            queryset = queryset.filter(materias=materia)
        return queryset
