from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=400)
    grupo = models.ForeignKey(Group,
                                on_delete=models.CASCADE,
                                null=True, 
                                blank=True)
    habilitado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    changed_by = models.ForeignKey(User,
                                   blank=True,
                                   null=True,
                                   on_delete=models.CASCADE)
    history = HistoricalRecords()
    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.nombre

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value