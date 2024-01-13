from django.contrib import admin
from .models import Modulo
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Modulo, SimpleHistoryAdmin)
