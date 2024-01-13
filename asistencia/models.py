from django.db import models
from materia.models import Materia
from carrera.models import Carrera
from alumno.models import Alumno

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Asistencia(models.Model):
    fecha = models.DateField()
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    alumnos = models.ManyToManyField(Alumno)
    habilitado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    changed_by = models.ForeignKey(User,
                                   blank=True,
                                   null=True,
                                   on_delete=models.CASCADE)
    history = HistoricalRecords()
    class Meta:
        ordering = ['id']

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value