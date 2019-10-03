
from django.urls import path, include
from apps.franquicias.views import home

urlpatterns = [
    path('', home, name='home'),
    path('productos/', include('apps.productos.urls', namespace='productos')),
    path('usuarios/', include('apps.usuarios.urls', namespace='usuarios')),
    path('ingredientes/', include('apps.ingredientes.urls', namespace='ingredientes')),
]