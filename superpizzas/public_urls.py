from django.contrib import admin
from django.urls import path,include
from apps.franquicias.views import home, nada

urlpatterns = [
    path('', nada, name='nada'),
    path('admin/', home, name='home'),
    path('admin/franquicias/', include('apps.franquicias.urls', namespace='franquicias')),
    #path('admin/', admin.site.urls),
]
