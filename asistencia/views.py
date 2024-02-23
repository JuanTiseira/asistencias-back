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
        

    # def create(self, request, *args, **kwargs):
    #     # Extraer datos del usuario del cuerpo de la solicitud
    #     if "rol" in request.data:
    #         rol_id = request.data['rol']
    #         rol = Rol.objects.get(pk=rol_id)
    #         request.data['rol'] = rol
        
    #     try:
    #         with transaction.atomic():
    #             user = None
    #             if request.data["username"] is not None and request.data["password"] is not None:
    #                 if len(request.data["username"]) > 0 and len(request.data["password"]) > 0:
    #                     # rol = request.data['rol']
    #                     # validate_password(request.data["password"])
    #                     user = User.objects.create_user(username=request.data["username"].upper(), password=request.data["password"])
    #                     if rol.grupo is not None:
    #                         user.groups.add(rol.grupo)
    #                         user.save()
        
    #             usuario = Usuario.objects.create(
    #                             rol=request.data['rol'], 
    #                             nombre=request.data['nombre'].upper(),
    #                             apellido=request.data['apellido'].upper(),
    #                             telefono=request.data['telefono'])
                
               
    #             if len(request.data['dni']) > 0:
    #                 usuario.dni = request.data['dni']
                    
    #             if len(request.data['direccion']) > 0:
    #                 usuario.direccion = request.data['direccion'].upper()
                    
    #             if len(request.data['fecha_nacimiento']) > 0:
    #                 usuario.fecha_nacimiento = request.data['fecha_nacimiento']
                    
    #             if len(request.data['email']) > 0:
    #                 usuario.email = request.data['email'].upper()
                    
    #             if user is not None:
    #                 usuario.user = user
                    
                
    #             usuario.changed_by = request.user
    #             usuario.save()
    #             usuario = UsuarioSerializer(usuario, context={'request': request}).data
    #             return Response(data={'success': True, 'message': "Usuario creado.", "data" : usuario},
    #                         status= status.HTTP_201_CREATED)
                
    #     except ValidationError as ex:
    #         return Response(data={'success': False, 'message': "No se pudo crear el usuario, contraseña inválida", 'error': str(ex)},
    #                         status= status.HTTP_400_BAD_REQUEST)
    #     except Exception as ex:
    #         if len(ex.args[0].split("DETAIL: "))>1:
    #             error = ex.args[0].split("DETAIL: ")[1]
    #         else:
    #             error = ex    
    #         return Response(data={'success': False, 'message': "No se pudo crear el usuario", 'error': str(error)},
    #                         status= status.HTTP_400_BAD_REQUEST)
    