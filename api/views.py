# En el archivo views.py de la aplicación usuarios
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from datetime import timedelta
from usuarios.models import Usuario
from rol.models import Rol

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import UntypedToken, TokenError

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        expiration_time = timedelta(minutes=1)

        rol_user = Usuario.objects.get(user=user)
        if not rol_user.habilitado:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
            'result':'Usuario deshabilitado'})
        
        token, created = Token.objects.get_or_create(user=user)

        token.save()


        # Personaliza la respuesta con información adicional
        return Response({
            'token': token.key,
            'username': user.username,
            'rol': user.usuario.rol.nombre,  # Ajusta esto según la relación de usuario y rol en tu modelo
        })

#prueba
class CustomObtainTokenPairView(TokenObtainPairView, ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.data.get('refresh', None)
        access = response.data.get('access', None)

        serializer = ObtainAuthToken.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        rol_user = Usuario.objects.get(user=user)
        if not rol_user.habilitado:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
            'result':'Usuario deshabilitado'})
        
        token, created = Token.objects.get_or_create(user=user)

        token.save()
        if refresh and access:
            refresh_token = RefreshToken(refresh)
            refresh_token.access_token.set_exp(lifetime=timedelta(minutes=15))  # Ajusta según tus necesidades
            response.data['refresh'] = str(refresh_token)
            response.data['access'] = str(refresh_token.access_token)

        return response


class JWTExpirationAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            raise AuthenticationFailed('Sin credenciales')

        try:
            # Accede al token JWT desde la cabecera de autorización
            token = auth_header.split(' ')[1]
            
            # Intenta decodificar el token
            UntypedToken(token)
        except TokenError as e:
            if isinstance(e, TokenError) and 'Token is expired' in str(e):
                raise AuthenticationFailed('Token expirado')
            else:
                raise AuthenticationFailed('Token no válido')

        # Retorna None para indicar que la autenticación es exitosa
        return None
