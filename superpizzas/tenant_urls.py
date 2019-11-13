
from django.urls import path, include
from apps.franquicias.views import home, inicio_tenants, configuraciones,informacion,renuncia
from apps.usuarios.views import inicio_sesion, cerrar_sesion,gestionar_cliente, check_email

urlpatterns = [
    path('', inicio_tenants, name='inicio_t'),
    path('admin/', home, name='home'),
    path('login/', inicio_sesion,name='login'), 
    path('accounts/', include('allauth.urls')),
    path('cerrar_sesion/',cerrar_sesion, name='cerrar_sesion'),
    path('admin/pizzas/', include('apps.pizzas.urls', namespace='pizzas')),
    path('admin/usuarios/', include('apps.usuarios.urls', namespace='usuarios')),
    path('registroclientes/',gestionar_cliente,name="registro"),  
    path('validate_email/', check_email, name='check_email'),  
    path('admin/ingredientes/', include('apps.ingredientes.urls', namespace='ingredientes')),
    path('admin/configuraciones/',configuraciones, name='configuraciones'),
    path('admin/info/',informacion,name='info'),
    path('renuncia/',renuncia,name='renuncia'),
]