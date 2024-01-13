from django.contrib import admin
from .models import EstadoAsistencia
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(EstadoAsistencia, SimpleHistoryAdmin)
