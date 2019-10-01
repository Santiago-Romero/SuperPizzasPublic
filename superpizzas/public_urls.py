from django.contrib import admin
from django.urls import path,include
from apps.franquicias.views import home

urlpatterns = [
    path('', home, name='home'),
    path('franquicias/', include('apps.franquicias.urls', namespace='franquicias')),
    path('admin/', admin.site.urls),
]
