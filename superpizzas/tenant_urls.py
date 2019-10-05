
from django.urls import path, include
from apps.franquicias.views import home, nada_tenant

urlpatterns = [
    path('', nada_tenant, name='nada_tenant'),
    path('admin/', home, name='home'),
    path('admin/productos/', include('apps.productos.urls', namespace='productos')),
    path('admin/usuarios/', include('apps.usuarios.urls', namespace='usuarios')),
    path('admin/ingredientes/', include('apps.ingredientes.urls', namespace='ingredientes')),
]