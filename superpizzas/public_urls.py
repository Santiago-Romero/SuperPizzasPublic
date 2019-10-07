from django.contrib import admin
from django.urls import path,include
from apps.franquicias.views import home, inicio_franquicia

urlpatterns = [
    path('', inicio_franquicia, name='nada'),
    path('admin/', home, name='home'),
    path('admin/franquicias/', include('apps.franquicias.urls', namespace='franquicias')),
    #path('admin/', admin.site.urls),
]
