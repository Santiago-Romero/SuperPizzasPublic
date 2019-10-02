from django.urls import path
from .views import *

app_name = 'productos'
urlpatterns = [
    path('registrar/', gestionar_producto, name='registrar'),
    path('modificar/<int:id_producto>/', gestionar_producto, name='modificar'),
    path('eliminar/<int:id_producto>/', eliminar_producto, name='eliminar'),
]