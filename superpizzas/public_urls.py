from django.contrib import admin
from django.urls import path,include
from apps.franquicias.views import home, inicio_franquicia,compra_franquicia


urlpatterns = [
    path('', inicio_franquicia, name='inicio'),
    path('compra/<str:tipo>', compra_franquicia, name='compra'),
    path('admin/', home, name='home'),
    path('admin/franquicias/', include('apps.franquicias.urls', namespace='franquicias')),
    #path('admin/', admin.site.urls),
]
