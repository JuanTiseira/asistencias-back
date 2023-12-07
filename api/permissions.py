from rest_framework.permissions import DjangoModelPermissions


class CustomDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        print("request", request)
        # Permite a los usuarios autenticados realizar cualquier acción,
        # pero solo permite a los administradores realizar acciones de escritura.
        if request.user and request.user.is_authenticated:
            return request.user.usuario.rol.nombre == 'ADMIN'
        return False
