# En el archivo views.py de la aplicación usuarios
from rest_framework import status, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from datetime import timedelta
from usuarios.models import Usuario
from rol.models import Rol

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .authentication import token_expire_handler, expires_in

class CustomObtainAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data,
                                            context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            
            expiration_time = timedelta(minutes=1)

            rol_user = Usuario.objects.get(user=user)
            if not rol_user.habilitado:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                'result':'Usuario deshabilitado'
                })
            
            token, created = Token.objects.get_or_create(user=user)
            is_expired, token = token_expire_handler(token)



            # Personaliza la respuesta con información adicional
            return Response({
                'token': token.key,
                'username': user.username,
                'rol': user.usuario.rol.nombre,  # Ajusta esto según la relación de usuario y rol en tu modelo
            })
        
        except Exception as e:
            return Response(data={'success': False, 'message': str(e)}, status=status.HTTP_403_FORBIDDEN)