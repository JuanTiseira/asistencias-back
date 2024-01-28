from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from api.permissions import CustomDjangoModelPermissions
from rol.models import Rol
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework.decorators import action

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.DjangoModelPermissions, CustomDjangoModelPermissions, ]
    authentication_classes = [TokenAuthentication]


    @action(detail=False, methods=['POST'])
    def edit_user(self, request):            
        try:
            with transaction.atomic():
                if "rol" in request.data:
                    rol_data = request.data['rol']
                    rol_id = rol_data["id"]
                    rol = Rol.objects.get(pk=rol_id)
                    request.data['rol'] = rol

                if request.data["id"] is not None:
                    id = request.data["id"]
                    usuario = Usuario.objects.get(pk=id)
                
                    if (request.data['rol']):
                        usuario.rol = request.data['rol']
                    
                    if len(request.data['apellido']) > 0:
                        usuario.apellido = request.data['apellido']

                    if len(request.data['nombre']) > 0:
                        usuario.nombre = request.data['nombre']

                    if (request.data['dni']):
                        usuario.dni = request.data['dni']
                        
                    if len(request.data['direccion']) > 0:
                        usuario.direccion = request.data['direccion'].upper()
                        
                    if len(request.data['fecha_nacimiento']) > 0:
                        usuario.fecha_nacimiento = request.data['fecha_nacimiento']
                        
                    if len(request.data['email']) > 0:
                        usuario.email = request.data['email'].upper()

                    if len(request.data['telefono']) > 0:
                        usuario.telefono = request.data['telefono']
                    
                if "username" in request.data and request.data["username"] is not None and \
                        "password" in request.data and request.data["password"] is not None:
                    if len(request.data["username"]) > 0 and len(request.data["password"]) > 0:
                        print(usuario.user.id)
                        user_id = usuario.user.id
                        user = User.objects.get(pk=user_id)
                        user.username = request.data["username"].upper()
                        new_password = request.data["password"]
                        user.set_password(new_password)
                        user.save()
                        if rol.grupo is not None:
                            print(user.groups.all(), rol.grupo)
                            user.groups.set([rol.grupo])
                            print(user.groups.all(), user.username)
                            user.save()
                
                usuario.changed_by = request.user
                usuario.save()
                usuario = UsuarioSerializer(usuario, context={'request': request}).data
                return Response(data={'success': True, 'message': "Usuario modificado.", "data" : usuario},
                            status= status.HTTP_201_CREATED)
        
        except ValidationError as ex:
            return Response(data={'success': False, 'message': "No se pudo modificar el usuario, contraseña inválida", 'error': str(ex)},
                            status= status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            if len(ex.args[0].split("DETAIL: "))>1:
                error = ex.args[0].split("DETAIL: ")[1]
            else:
                error = ex    
            return Response(data={'success': False, 'message': "No se pudo modificar el usuario", 'error': str(error)},
                            status= status.HTTP_400_BAD_REQUEST)
        
    def create(self, request, *args, **kwargs):
        # Extraer datos del usuario del cuerpo de la solicitud
        if "rol" in request.data:
            rol_id = request.data['rol']
            rol = Rol.objects.get(pk=rol_id)
            request.data['rol'] = rol
        
        try:
            with transaction.atomic():
                user = None
                if request.data["username"] is not None and request.data["password"] is not None:
                    if len(request.data["username"]) > 0 and len(request.data["password"]) > 0:
                        # rol = request.data['rol']
                        # validate_password(request.data["password"])
                        user = User.objects.create_user(username=request.data["username"].upper(), password=request.data["password"])
                        if rol.grupo is not None:
                            user.groups.add(rol.grupo)
                            user.save()
        
                usuario = Usuario.objects.create(
                                rol=request.data['rol'], 
                                nombre=request.data['nombre'].upper(),
                                apellido=request.data['apellido'].upper(),
                                telefono=request.data['telefono'])
                
               
                if len(request.data['dni']) > 0:
                    usuario.dni = request.data['dni']
                    
                if len(request.data['direccion']) > 0:
                    usuario.direccion = request.data['direccion'].upper()
                    
                if len(request.data['fecha_nacimiento']) > 0:
                    usuario.fecha_nacimiento = request.data['fecha_nacimiento']
                    
                if len(request.data['email']) > 0:
                    usuario.email = request.data['email'].upper()
                    
                if user is not None:
                    usuario.user = user
                    
                
                usuario.changed_by = request.user
                usuario.save()
                usuario = UsuarioSerializer(usuario, context={'request': request}).data
                return Response(data={'success': True, 'message': "Usuario creado.", "data" : usuario},
                            status= status.HTTP_201_CREATED)
                
        except ValidationError as ex:
            return Response(data={'success': False, 'message': "No se pudo crear el usuario, contraseña inválida", 'error': str(ex)},
                            status= status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            if len(ex.args[0].split("DETAIL: "))>1:
                error = ex.args[0].split("DETAIL: ")[1]
            else:
                error = ex    
            return Response(data={'success': False, 'message': "No se pudo crear el usuario", 'error': str(error)},
                            status= status.HTTP_400_BAD_REQUEST)
    