from django.db import models
from materia.models import Materia
from carrera.models import Carrera
from alumno.models import Alumno
from estado_asistencia.models import EstadoAsistencia
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Asistencia(models.Model):
    fecha = models.DateField()
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    alumnos = models.ManyToManyField(Alumno, through='AsistenciaAlumno')
    habilitado = models.BooleanField(default=True)
    cantidad_presentes = models.PositiveIntegerField(default=0)
    cantidad_ausentes = models.PositiveIntegerField(default=0)
    cantidad_justificados = models.PositiveIntegerField(default=0)
    cantidad_tardanza = models.PositiveIntegerField(default=0)

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

    def actualizar_cantidad_alumnos(self):
        # Obtener la cantidad de alumnos presentes
        presentes = self.asistenciaalumno_set.filter(estado__nombre='PRESENTE').count()
        # Obtener la cantidad de alumnos ausentes
        ausentes = self.asistenciaalumno_set.filter(estado__nombre='AUSENTE').count()
        # Actualizar los campos en el modelo de Asistencia
        justificados = self.asistenciaalumno_set.filter(estado__nombre='JUSTIFICADO').count()
        tardanza = self.asistenciaalumno_set.filter(estado__nombre='TARDANZA').count()
        print("·@@@@@@@@@", presentes, ausentes, justificados, tardanza)
        
        self.cantidad_presentes = presentes
        self.cantidad_ausentes = ausentes
        self.cantidad_justificados = justificados
        self.cantidad_tardanza = tardanza
        self.save()

class AsistenciaAlumno(models.Model):
    asistencia = models.ForeignKey(Asistencia, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoAsistencia, on_delete=models.CASCADE, null=True)
    observaciones = models.CharField(max_length=400, null=True, blank=True)

    class Meta:
        db_table = 'asistencia_asistencia_alumnos'
        unique_together = (('asistencia', 'alumno'),)