from django.db import models

from rol.models import Rol

from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords


class Usuario(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    rol = models.ForeignKey(Rol,
                            on_delete=models.CASCADE,
                            null=False,
                            blank=False)                             
    dni = models.BigIntegerField(null=True,
                                 blank=True)
    nombre = models.CharField(max_length=50,
                              null=False,
                              blank=False)
    apellido = models.CharField(max_length=50,
                                null=False,
                                blank=False)
    direccion = models.CharField(max_length=100,
                                 null=True,
                                 blank=True)
    fecha_nacimiento = models.DateField(null=True,
                                        blank=True)
    email = models.EmailField(unique=True,
                              null=True,
                              blank=True)
    telefono = models.CharField(max_length=50,
                                null=False,
                                blank=False)
    habilitado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    changed_by = models.ForeignKey(User,
                                   blank=True,
                                   null=True,
                                   on_delete=models.CASCADE,
                                   related_name= 'changed_by')
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.nombre + ' ' + self.apellido
    
    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value
        
    def isAdmin(self):
        print(self.rol.nombre)
        return self.rol.nombre == "ROL_ADMIN"
    
    def hasPermision(self):
        print(self.rol.nombre)
        return self.rol.nombre == "ROL_PRECEPTOR" or self.rol.nombre == "ROL_PROFESOR" or self.isAdmin()
