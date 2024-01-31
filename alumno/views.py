from .models import Alumno
from rest_framework import viewsets, status
from rest_framework import permissions
from .serializers import AlumnoSerializer
from rest_framework.authentication import TokenAuthentication
from api.permissions import CustomDjangoModelPermissions 
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdminOrReadOnly
from rest_framework.response import Response
from django.db import transaction
from django.core.exceptions import ValidationError
from carrera.models import Carrera

class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
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


    def create(self, request, *args, **kwargs):
        # Extraer datos del usuario del cuerpo de la solicitud
        try:
            with transaction.atomic():
                
                usuario = Alumno.objects.create( 
                                nombre=request.data['nombre'].upper(),
                                apellido=request.data['apellido'].upper(),
                                telefono=request.data['telefono'])
                
                if 'dni' in request.data:
                    usuario.dni = request.data['dni']
                    
                if 'direccion' in request.data:
                    usuario.direccion = request.data['direccion'].upper()
                    
                if 'fecha_nacimiento' in request.data:
                    usuario.fecha_nacimiento = request.data['fecha_nacimiento']
                    
                if 'email' in request.data:
                    usuario.email = request.data['email'].upper()

                if 'carreras' in request.data:
                    carrera = request.data['carreras']
                    for i in carrera:
                        print(i)
                        carreras = Carrera.objects.get(pk=i)
                        print(carreras)
                        usuario.carreras.add(carreras)

                usuario.changed_by = request.user
                usuario.save()
                usuario = AlumnoSerializer(usuario, context={'request': request}).data
                return Response(data={'success': True, 'message': "Alumno creado.", "data" : usuario},
                            status= status.HTTP_201_CREATED)
                
        except ValidationError as ex:
            return Response(data={'success': False, 'message': "No se pudo crear el alumno, contraseña inválida", 'error': str(ex)},
                            status= status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            if len(ex.args[0].split("DETAIL: "))>1:
                error = ex.args[0].split("DETAIL: ")[1]
            else:
                error = ex    
            return Response(data={'success': False, 'message': "No se pudo crear el alumno", 'error': str(error)},
                            status= status.HTTP_400_BAD_REQUEST)