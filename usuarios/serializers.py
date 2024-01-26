from rest_framework import serializers
from .models import Usuario
from rol.serializers import RolSerializer
from drf_writable_nested import WritableNestedModelSerializer

class UsuarioSerializer(WritableNestedModelSerializer, serializers.HyperlinkedModelSerializer):
    rol = RolSerializer()
    class Meta:
        model = Usuario
        fields = ['id', 'url', 'nombre', 'apellido', 'dni', 'direccion', 'fecha_nacimiento', 'email', 'telefono', 'rol']
