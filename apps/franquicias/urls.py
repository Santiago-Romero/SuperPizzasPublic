from django.urls import path
from .views import *

app_name = 'franquicias'
urlpatterns = [
    path('registrar/', registrar_franquicia, name='registrar'),
    path('modificar/<int:id_franquicia>/', modificar_franquicia, name='modificar'),
]