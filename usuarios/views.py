from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from api.permissions import CustomDjangoModelPermissions


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.DjangoModelPermissions, CustomDjangoModelPermissions, ]
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        # Extraer datos del usuario del cuerpo de la solicitud
        user_data = {
            'username': request.data.get('nombre'),  # Ajusta cómo quieres asignar el nombre de usuario
            'password': request.data.get('password'),  # Ajusta cómo manejas la contraseña
            'email': request.data.get('email', ''),  # Ajusta según tus necesidades
        }

        # Crear un nuevo usuario
        user = User.objects.create_user(**user_data)

        # Agregar el usuario recién creado al cuerpo de la solicitud
        request.data['user'] = user.id

        # Llamar al método create del serializador para manejar la creación del objeto Usuario
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
