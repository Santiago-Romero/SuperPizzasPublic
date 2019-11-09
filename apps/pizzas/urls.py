from django.urls import path
from .views import *

app_name = 'pizzas'
urlpatterns = [
    path('registrar/', gestionar_pizza, name='registrar'),
    path('modificar/<int:id_pizza>/', gestionar_pizza, name='modificar'),
    path('eliminar/<int:id_pizza>/', eliminar_pizza, name='eliminar'),
    path('info/', informacion, name='info'),
]