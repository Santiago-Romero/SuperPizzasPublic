from django.urls import path
from .views import *

app_name = 'usuarios'
urlpatterns = [
    path('registrar/', gestionar_usuario, name='registrar'),
    path('modificar/<int:id_usuario>/', gestionar_usuario, name='modificar'),
    path('eliminar/<int:id_usuario>/', eliminar_usuario, name='eliminar')    
]