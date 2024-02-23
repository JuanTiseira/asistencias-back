from django.db import models
from materia.models import Materia
from carrera.models import Carrera

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)
    email = models.CharField(max_length=400)
    direccion = models.CharField(max_length=400)
    telefono = models.CharField(max_length=20)
    materias = models.ManyToManyField(Materia, through='AsistenciaMateria')
    carreras = models.ManyToManyField(Carrera, blank=True)
    fecha_nacimiento = models.DateField(null=True)
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

    def get_estado(self):
        # Lógica para obtener el estado del alumno, por ejemplo:
        estado_asistencia = self.asistenciaalumno_set.first().estado.nombre
        return estado_asistencia
    
class AsistenciaMateria(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=[('Regular', 'Regular'), ('Irregular', 'Irregular'), ('Promocionado', 'Promocionado')], default='Regular')
    asistencias = models.PositiveIntegerField(default=0)