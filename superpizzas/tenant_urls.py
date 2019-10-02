
from django.urls import path, include
from apps.franquicias.views import home

urlpatterns = [
    path('', home, name='home'),
    path('productos/', include('apps.productos.urls', namespace='productos')),
]