from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asistencia.models import Asistencia, AsistenciaAlumno
from alumno.models import AsistenciaMateria

@receiver(post_save, sender=Asistencia)
def actualizar_estado_alumno(sender, instance, created,**kwargs):
    for alumno in instance.alumnos.all():
        for materia in alumno.materias.all():
            asistencia_materia, created = AsistenciaMateria.objects.get_or_create(alumno=alumno, materia=materia)
            asistencia_materia.asistencias = Asistencia.objects.filter(alumnos=alumno, materia=materia).count()
            asistencia_materia.estado = determinar_estado(asistencia_materia.asistencias)  # Implementa tu lógica de determinar el estado
            asistencia_materia.save()

@receiver(post_save, sender=AsistenciaAlumno)
@receiver(post_delete, sender=AsistenciaAlumno)
def actualizar_cantidad_alumnos(sender, instance, **kwargs):
    asistencia = instance.asistencia
    presentes = asistencia.asistenciaalumno_set.filter(estado__nombre='PRESENTE').count()
    ausentes = asistencia.asistenciaalumno_set.filter(estado__nombre='AUSENTE').count()
    justificados = asistencia.asistenciaalumno_set.filter(estado__nombre='JUSTIFICADO').count()
    tardanza = asistencia.asistenciaalumno_set.filter(estado__nombre='TARDANZA').count()

    asistencia.cantidad_presentes = presentes
    asistencia.cantidad_ausentes = ausentes
    asistencia.cantidad_justificados = justificados
    asistencia.cantidad_tardanza = tardanza
    asistencia.save()

def determinar_estado(self):
    total_asistencias = Asistencia.objects.filter(alumnos=self).count()
    # Aquí puedes implementar tu lógica para determinar el estado del alumno según las asistencias.
    # Por ejemplo, si el alumno tiene más del 80% de asistencias, puede ser "Regular".

    # Actualizar el estado del alumno
    if total_asistencias >= 80:
        self.estado = 'Regular'
    else:
        self.estado = 'Irregular'
    self.save()