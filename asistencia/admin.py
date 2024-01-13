# En el archivo admin.py
from django.contrib import admin
from .models import Asistencia

class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'carrera', 'materia', 'get_alumnos', 'habilitado', 'created_at')
    search_fields = ('id', 'fecha', 'carrera__nombre', 'materia__nombre', 'alumnos__nombre', 'alumnos__apellido')

    def get_alumnos(self, obj):
        return ", ".join([alumno.nombre for alumno in obj.alumnos.all()])
    get_alumnos.short_description = 'Alumnos'

admin.site.register(Asistencia, AsistenciaAdmin)
