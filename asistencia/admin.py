# # En el archivo admin.py
# from django.contrib import admin
# from .models import Asistencia

# class AsistenciaAdmin(admin.ModelAdmin):
#     list_display = ('id', 'fecha', 'carrera', 'materia', 'get_alumnos', 'estado', 'habilitado', 'created_at')
#     search_fields = ('id', 'fecha', 'carrera__nombre', 'materia__nombre', 'alumnos__nombre', 'alumnos__apellido')

#     def get_alumnos(self, obj):
#         return ", ".join([alumno.nombre for alumno in obj.alumnos.all()])
#     get_alumnos.short_description = 'Alumnos'

# admin.site.register(Asistencia, AsistenciaAdmin)


from django.contrib import admin
from .models import Asistencia, AsistenciaAlumno

class AsistenciaAlumnoInline(admin.TabularInline):
    model = AsistenciaAlumno
    extra = 1

class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'carrera', 'materia', 'get_alumnos', 'habilitado', 'created_at')
    search_fields = ('id', 'fecha', 'carrera__nombre', 'materia__nombre', 'alumnos__nombre', 'alumnos__apellido')

    inlines = [
        AsistenciaAlumnoInline,
    ]

    def get_alumnos(self, obj):
        return ", ".join([alumno.nombre for alumno in obj.alumnos.all()])
    get_alumnos.short_description = 'Alumnos'

    fieldsets = (
        (None, {
            'fields': ('fecha', 'carrera', 'materia', 'habilitado')
        }),
    )

admin.site.register(Asistencia, AsistenciaAdmin)
