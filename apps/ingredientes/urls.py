from django.urls import path
from .views import *

app_name = 'ingredientes'
urlpatterns = [
    path('registrar/', gestionar_ingrediente, name='registrar'),
    path('modificar/<int:id_ingrediente>/', gestionar_ingrediente, name='modificar'),
    path('eliminar/<int:id_ingrediente>/', eliminar_ingrediente, name='eliminar'),
]