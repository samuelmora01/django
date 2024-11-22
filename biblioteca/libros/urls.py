from django.urls import path
from . import views  # Asegúrate de que views esté importado correctamente

urlpatterns = [
    path('', views.home, name='home'),  # La vista 'home' debe estar definida en views.py
     path("buscar/", views.buscar_libros, name="buscar_libros"),
]
