from .models import Carrera
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import CarreraSerializer
from rest_framework.authentication import TokenAuthentication
from api.permissions import CustomDjangoModelPermissions 
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdminOrReadOnly
from rest_framework.response import Response

class CarreraViewSet(viewsets.ModelViewSet):
    queryset = Carrera.objects.all()
    serializer_class = CarreraSerializer
    # permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        queryset = Carrera.objects.all()
        nombre = self.request.query_params.get('nombre')
        descripcion = self.request.query_params.get('descripcion')
        habilitado = self.request.query_params.get('habilitado')

        if habilitado is not None:
            queryset = queryset.filter(habilitado=habilitado)
        else:
            queryset = queryset.filter(habilitado=True)

        if nombre is not None:
            queryset = queryset.filter(nombre=nombre)
        if descripcion is not None:
            queryset = queryset.filter(descripcion=descripcion)

        return queryset
