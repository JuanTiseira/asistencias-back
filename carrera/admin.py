from django.contrib import admin
from .models import Carrera
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Carrera, SimpleHistoryAdmin)
