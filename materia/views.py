from .models import Materia
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ModuloSerializer
from rest_framework.authentication import TokenAuthentication
from api.permissions import CustomDjangoModelPermissions 
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdminOrReadOnly
from rest_framework.response import Response

class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = ModuloSerializer
    # permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        queryset = Materia.objects.all()
        nombre = self.request.query_params.get('nombre')
        descripcion = self.request.query_params.get('descripcion')
        carrera = self.request.query_params.get('carrera')
        modulos = self.request.query_params.get('modulos')
        anual = self.request.query_params.get('anual')
        habilitado = self.request.query_params.get('habilitado')

        if habilitado is not None:
            queryset = queryset.filter(habilitado=habilitado)
        else:
            queryset = queryset.filter(habilitado=True)

        if nombre is not None:
            queryset = queryset.filter(nombre=nombre)
        if descripcion is not None:
            queryset = queryset.filter(descripcion=descripcion)
        if carrera is not None:
            queryset = queryset.filter(carrera=carrera)
        if modulos is not None:
            queryset = queryset.filter(modulos=modulos)
        if anual is not None:
            queryset = queryset.filter(anual=anual)
        return queryset
