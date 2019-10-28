
from django.urls import path, include
from apps.franquicias.views import home, inicio_tenants
from apps.usuarios.views import login_view

urlpatterns = [
    path('', inicio_tenants, name='inicio_t'),
    path('admin/', home, name='home'),
    path('login/', login_view,name='login'), 
    path('admin/pizzas/', include('apps.pizzas.urls', namespace='pizzas')),
    path('admin/usuarios/', include('apps.usuarios.urls', namespace='usuarios')),
    path('admin/ingredientes/', include('apps.ingredientes.urls', namespace='ingredientes')),
]