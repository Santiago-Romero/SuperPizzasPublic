from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.http import HttpResponse
from apps.usuarios.forms import UsuarioForm, UserForm
from django_tenants.utils import schema_context
from django.contrib.auth.models import User
from apps.usuarios.models import Usuario
from apps.pizzas.models import Pizza
from tenant_schemas.utils import *
from django.http import HttpRequest
from rolepermissions.roles import assign_role
from apps.franquicias.models import Franquicia
import json
import os

def home(request):

    #Si usario es anonimo? 
    if request.user.is_anonymous:
        return redirect('/')
    #Validacion del Formulario a traves del metodo POST
    else:
        id_usuario = request.user.id

        perfil = Usuario.objects.get(user=id_usuario)

        if perfil.rol == 'a':
            return render(request, 'base.html', {})
        else:
            return redirect('/login')

def home_admin(request):
    #Si usario es anonimo? 
    if request.user.is_anonymous:
        return redirect('/')
    #Validacion si es superusuario
    elif request.user.is_superuser:
        return render(request, 'base.html', {})
    else:
        return redirect('/')

def inicio_franquicia(request):
    return render(request, 'landingpage/index.html', {})

def compra_franquicia(request,tipo):
    
    dominios = Dominio.objects.exclude(tenant__schema_name='public').select_related('tenant')

    tipoir=TipoFranquicia.objects.get(nombre=tipo)

    if request.method == 'POST':

        form = FranquiciaForm(request.POST,prefix="form1",initial={'tipo': tipoir})
        formUsuario = UsuarioForm(request.POST,prefix="form2",initial={'rol': 'a'})
        formUserDjango = UserForm(request.POST,prefix="form3")

        print(str(request.POST))

        if form.is_valid() and formUserDjango.is_valid():
            
            try:

                with transaction.atomic():
                    franquicia = form.save()
                   
                    Dominio.objects.create(domain='%s%s' % (franquicia.schema_name, settings.DOMAIN), is_primary=True, tenant=franquicia)

                    with schema_context(franquicia.schema_name):

                        #CREACIÓN DEL USUARIO DJANGO
                        
                        usuario = formUserDjango.save(commit=False)
                        
                        usuario = User(username=request.POST['form3-username'], email=request.POST['form3-email'], first_name=request.POST['form3-first_name'], last_name=request.POST['form3-last_name'])
                        
                        usuario.set_password(request.POST['form3-password1'])
                        
                        usuario.save()

                        assign_role(usuario,'administrador')

                        #CREACION DEL USUARIO - INFORMACIÓN ADICIONAL

                        perfil = Usuario(user=usuario,cc=request.POST['form2-cc'],telefono=request.POST['form2-telefono'],pais=request.POST['form2-pais'],nombre_banco=request.POST['form2-nombre_banco'],fecha_vencimiento=request.POST['form2-fecha_vencimiento'],tipo_tarjeta=request.POST['form2-tipo_tarjeta'],numero_tarjeta=request.POST['form2-numero_tarjeta'],cvv=request.POST['form2-cvv'],rol='a')

                        perfil.save()
                        
            except Exception as e: 
                print(e,"error")
            context={
                'nombre': form.data.get('form1-nombre'),
                'schema': form.data.get('form1-schema_name'),
            }
            return render(request,'landingpage/comprado.html',context)
        else:
            print(str(formUsuario.errors))
            print(str(formUserDjango.errors))
            print(str(formUserDjango.errors))
            messages.error(request, "Por favor verificar los campos en rojo")
    else:
        form = FranquiciaForm(prefix="form1",initial={'tipo': tipoir})
        formUsuario = UsuarioForm(prefix="form2",initial={'rol': 'a'})
        formUserDjango = UserForm(prefix="form3")
    context = {
        'form1': form,
        'form2': formUsuario,
        'form3': formUserDjango,
        'dominios': dominios,
        'tipo': tipoir}
    return render(request, 'landingpage/compra.html', context)

def inicio_tenants(request):
    nombreFranquicia= request.tenant.nombre 
    franquicia = Franquicia.objects.get(schema_name=nombreFranquicia)
    context = {
        'pizzas':Pizza.objects.all(),
        'especiales': Pizza.objects.filter(especial=True,enventa=True),
        'enventas': Pizza.objects.filter(enventa=True),
        'franquicia':request,
        'colorprimario': json.loads(franquicia.configuracion)['colorprimario'],
        'colorsecundario': json.loads(franquicia.configuracion)['colorsecundario'],
        'tamanioletra': json.loads(franquicia.configuracion)['tamanioletra'],
        'tamanioletraX2': int(json.loads(franquicia.configuracion)['tamanioletra'])*2,
        'tamanioletraXpix': int(json.loads(franquicia.configuracion)['tamanioletra'])/10 +3,
        'logo':  franquicia.media,
    }
    return render(request, 'tenant/index.html', context)


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


def check_schema(request):
    if HttpRequest.is_ajax and request.method == 'GET':        
        schema_name = request.GET.get('form1-schema_name')       
        if schema_exists(schema_name):
            print('duplicate')  # have this for checking in console
            return HttpResponse('false')
        else:
            print("no duplicate")
            print(str(schema_name))
            return HttpResponse('true')
    else:
        return HttpResponse("Zero")
    
def configuraciones(request):
    franquicia= request.tenant.nombre 
    datosfran = Franquicia.objects.get(schema_name=franquicia)
    contexto = {'franquicia': datosfran, 
    'colorprimario': json.loads(datosfran.configuracion)['colorprimario'],
    'colorsecundario': json.loads(datosfran.configuracion)['colorsecundario'],
    'logo':  datosfran.media,
    'tamanioletra': json.loads(datosfran.configuracion)['tamanioletra']
    }

    if request.method == 'POST':
        datosfran.configuracion = '{\"colorprimario\":\"#'+ request.POST.get("colorpimario") +'\",\"colorsecundario\":\"#'+ request.POST.get("colorsecundario") +'\", \"tamanioletra\":'+ request.POST.get("tamanioLetra") +'}'
        
        if request.FILES.get('inputFileLogoConfig') != None:
            pathLogoAnterior = datosfran.media
            if pathLogoAnterior != 'media/logos-franquicias/1_logo_default.png':
                try:
                    os.remove(datosfran.media.path)
                except:
                    print('***No se pudo Eliminar imagen anterior***')
            datosfran.media = request.FILES.get('inputFileLogoConfig')
        try:    
            datosfran.save()
            messages.success(request, 'Configuraciones guardadas correctamente')
        except:
            messages.error(request, 'Error al intentar guardar configuraciones')

        franquicia= request.tenant.nombre 
        datosfran = Franquicia.objects.get(schema_name=franquicia)
        contexto = {'franquicia': datosfran, 
        'colorprimario': json.loads(datosfran.configuracion)['colorprimario'],
        'colorsecundario': json.loads(datosfran.configuracion)['colorsecundario'],
        'logo':  datosfran.media,
        'tamanioletra': json.loads(datosfran.configuracion)['tamanioletra']
        }
    return render(request,'franquicias/configuraciones.html', contexto)
        
    
