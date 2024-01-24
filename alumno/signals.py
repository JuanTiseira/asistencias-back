from django.db.models.signals import post_save
from django.dispatch import receiver
from asistencia.models import Asistencia
from alumno.models import AsistenciaMateria

@receiver(post_save, sender=Asistencia)
def actualizar_estado_alumno(sender, instance, **kwargs):
    for alumno in instance.alumnos.all():
        for materia in alumno.materias.all():
            asistencia_materia, created = AsistenciaMateria.objects.get_or_create(alumno=alumno, materia=materia)
            asistencia_materia.asistencias = Asistencia.objects.filter(alumnos=alumno, materia=materia).count()
            asistencia_materia.estado = determinar_estado(asistencia_materia.asistencias)  # Implementa tu lógica de determinar el estado
            asistencia_materia.save()

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