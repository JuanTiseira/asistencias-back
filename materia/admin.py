from django.contrib import admin
from .models import Materia
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Materia, SimpleHistoryAdmin)
