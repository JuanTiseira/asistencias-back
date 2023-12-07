from django.contrib import admin
from .models import Rol
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Rol, SimpleHistoryAdmin)
