
from django.urls import path
from apps.franquicias.views import nada

urlpatterns = [
    path('', nada, name='nada'),
]