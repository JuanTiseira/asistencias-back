"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.urls import include, path, re_path
from .views import CustomObtainAuthToken

from usuarios import views as user_views
from rol import views as rol_views
from carrera import views as carrera_views
from modulo import views as modulo_views
from materia import views as materia_views


router = routers.DefaultRouter()
router.register(r'usuarios', user_views.UsuarioViewSet)
router.register(r'rol', rol_views.RolViewSet)
router.register(r'carrera', carrera_views.CarreraViewSet)
router.register(r'modulo', modulo_views.ModuloViewSet)
router.register(r'materia', materia_views.MateriaViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('login/', CustomObtainAuthToken.as_view()),
]
