from django.contrib import admin
from django.urls import path,include
from apps.franquicias.views import *
from apps.usuarios.views import inicio_sesion_admin, cerrar_sesion, check_email


urlpatterns = [
    path('', inicio_franquicia, name='inicio'),
    path('compra/<str:tipo>', compra_franquicia, name='compra'),
    path('accounts/', include('allauth.urls')),
    path('admin/', home_admin, name='home'),
    #path('admin/',admin.site.urls),
    path('login/', inicio_sesion_admin,name='login'), 
    path('cerrar_sesion/',cerrar_sesion, name='cerrar_sesion'),    
    path('validate/', check_schema, name='check_schema'),  
    path('validate_email/', check_email, name='check_email'),  
    path('admin/franquicias/', include('apps.franquicias.urls', namespace='franquicias')),
    path('admin/metricas/', metricas, name='metricas'),
]
