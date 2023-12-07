from django.contrib import admin
from .models import Usuario

from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Usuario, SimpleHistoryAdmin)
