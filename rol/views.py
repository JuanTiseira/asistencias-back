from .models import Rol

from rest_framework import viewsets
from rest_framework import permissions
from .serializers import RolSerializer
from rest_framework.authentication import TokenAuthentication
from api.permissions import CustomDjangoModelPermissions


class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [permissions.DjangoModelPermissions, CustomDjangoModelPermissions]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        queryset = Rol.objects.all()
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
