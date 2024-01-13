
# En el archivo admin.py de la aplicación Alumno
from django.contrib import admin
from .models import Alumno

class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'get_carreras', 'get_materias')

    def get_carreras(self, obj):
        return ", ".join([c.nombre for c in obj.carreras.all()])
    get_carreras.short_description = 'Carreras'

    def get_materias(self, obj):
        return ", ".join([m.nombre for m in obj.materias.all()])
    get_materias.short_description = 'Materias'

admin.site.register(Alumno, AlumnoAdmin)
