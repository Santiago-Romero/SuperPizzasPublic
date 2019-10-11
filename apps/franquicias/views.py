from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.http import HttpResponse
from apps.usuarios.forms import UsuarioForm
from django_tenants.utils import schema_context

def home(request):
    return render(request, 'base.html', {})

def inicio_franquicia(request):
    return render(request, 'landingpage/index.html', {})

def compra_franquicia(request,tipo):
    dominios = Dominio.objects.exclude(tenant__schema_name='public').select_related('tenant')
    tipoir=TipoFranquicia.objects.get(nombre=tipo)
    form = FranquiciaForm(request.POST,prefix="form1")
    formUser = UsuarioForm(request.POST,prefix="form2")
    if request.method == 'POST':
        if form.is_valid() or formUser.is_valid():
            try:
                with transaction.atomic():
                    franquicia = form.save()
                    Dominio.objects.create(domain='%s%s' % (franquicia.schema_name, settings.DOMAIN), is_primary=True, tenant=franquicia)
                    messages.success(request, "Se ha registrado correctamente la franquicia")
                    with schema_context(franquicia.schema_name):
                        usuario=formUser.save() 
            except Exception:
                messages.error(request, 'Ha ocurrido un error durante la creación de la franquicia, se aborto la operación')
            return redirect('/compra/{}'.format(tipoir))
        else:
            messages.error(request, "Por favor verificar los campos en rojo")
    else:
        form = FranquiciaForm(prefix="form1")
        formUser = UsuarioForm(prefix="form2")
    context = {
    'form1': form,
    'form2': formUser,
    'dominios': dominios,
    'tipo': tipoir}
    return render(request, 'landingpage/compra.html', context)

def nada_tenant(request):
    print(request.tenant)
    return HttpResponse("<h2>Aqui iría la págia principal donde se venden las pizzas de cada tenant, por ahora ir a <a href='http://{d}.localhost:8000/admin/'>http://{d}.localhost:8000/admin/</a> para gestionar la franquicia</h2>".format(d=request.tenant.schema_name))


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