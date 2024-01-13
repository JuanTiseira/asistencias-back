from django.db import models
from carrera.models import Carrera
from modulo.models import Modulo
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=400)

    anual = models.BooleanField(default=True)
    
    carrera = models.ForeignKey(Carrera,
                            on_delete=models.CASCADE,
                            null=False,
                            blank=False)
    
    modulos = models.ManyToManyField(Modulo)

    habilitado = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User,
                                   blank=True,
                                   null=True,
                                   on_delete=models.CASCADE)
    
    history = HistoricalRecords()
    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.nombre

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value