from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.http import HttpResponse

def home(request):
    return render(request, 'base.html', {})

def nada(request):
    return HttpResponse("<h2>Aqui iría la págia principal donde se venden franquicias, por ahora ir a <a href='http://localhost:8000/admin/'>http://localhost:8000/admin/</a> para gestionar franquicias</h2>")

def nada_tenant(request):
    return HttpResponse("<h2>Aqui iría la págia principal donde se venden las pizzas de cada tenant, por ahora ir a <a href='http://localhost:8000/admin/'>http://[nombre_tenant].localhost:8000/admin/</a> para gestionar la franquicia</h2>")


def registrar_franquicia(request):
    """
    Permite registrar una franquicia (tenant) en el sistema
    :param request:
    :return:
    """
    dominios = Dominio.objects.exclude(tenant__schema_name='public').select_related('tenant')
    form = FranquiciaForm()
    if request.method == 'POST':
        form = FranquiciaForm(request.POST)
        if form.is_valid():
            try:
                """
                La operación se maneja como transaccional dado que involucra la creación de más de un objeto los cuales
                estan relacionados
                """
                with transaction.atomic():
                    franquicia = form.save()
                    """
                    Se crea el dominio y se le asocia información alojada en el tenant. En este punto es que sucede la
                    creación del esquema del tenant en la base de datos
                    """
                    Dominio.objects.create(domain='%s%s' % (franquicia.schema_name, settings.DOMAIN), is_primary=True, tenant=franquicia)
                    messages.success(request, "Se ha registrado correctamente la franquicia")
            except Exception:
                messages.error(request, 'Ha ocurrido un error durante la creación de la franquicia, se aborto la operación')
            return redirect('franquicias:registrar')
        else:
            messages.error(request, "Por favor verificar los campos en rojo")

    return render(request, 'franquicias/registrar.html', {'form': form, 'dominios': dominios})


def modificar_franquicia(request, id_franquicia):
    """
    Permite modificar parte de la información del tenant
    :param request:
    :param id_franquicia:
    :return:
    """
    franquicia = get_object_or_404(Franquicia, id=id_franquicia)
    dominios = Dominio.objects.exclude(tenant__schema_name='public').select_related('tenant')
    form = ModificarFranquiciaForm(instance=franquicia)
    if request.method == 'POST':
        form = ModificarFranquiciaForm(request.POST, instance=franquicia)
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha modificado correctamente la franquicia")
            return redirect('franquicias:registrar')
        else:
            messages.error(request, "Por favor verificar los campos en rojo")

    return render(request, 'franquicias/registrar.html', {'form': form, 'dominios': dominios})