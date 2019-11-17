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
from apps.pizzas.models import Pizza,Factura,Detalle
from apps.ingredientes.models import Ingrediente
from tenant_schemas.utils import *
from django.http import HttpRequest
from rolepermissions.roles import assign_role
from apps.franquicias.models import Franquicia
import json
import os
from datetime import date
from django.core import serializers
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy




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
    dominios = Dominio.objects.exclude(tenant__schema_name='public').select_related('tenant')
    tipos = TipoFranquicia.objects.all()
    return render(request, 'landingpage/index.html', {'tenants':dominios,'tipos':tipos})

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
                        
                        usuario = User(username=request.POST['form3-email'], email=request.POST['form3-email'], first_name=request.POST['form3-first_name'], last_name=request.POST['form3-last_name'])
                        
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

def reg_franquicia(request):
    dominios = Dominio.objects.exclude(tenant__schema_name='public').select_related('tenant')
    if request.method == 'POST':
        form = FranquiciaForm(request.POST,prefix="form1")
        formUsuario = UsuarioForm(request.POST,prefix="form2",initial={'rol': 'a'})
        formUserDjango = UserForm(request.POST,prefix="form3")
        print(str(request.POST))
        if form.is_valid() and formUserDjango.is_valid():
            try:
                with transaction.atomic():
                    franquicia = form.save()
                    Dominio.objects.create(domain='%s%s' % (franquicia.schema_name, settings.DOMAIN), is_primary=True, tenant=franquicia)
                    with schema_context(franquicia.schema_name):
                        usuario = formUserDjango.save(commit=False)
                        usuario = User(username=request.POST['form3-username'], email=request.POST['form3-email'], first_name=request.POST['form3-first_name'], last_name=request.POST['form3-last_name'])
                        usuario.set_password(request.POST['form3-password1'])
                        usuario.save()
                        assign_role(usuario,'administrador')
                        perfil = Usuario(user=usuario,cc=request.POST['form2-cc'],telefono=request.POST['form2-telefono'],pais=request.POST['form2-pais'],nombre_banco=request.POST['form2-nombre_banco'],fecha_vencimiento=request.POST['form2-fecha_vencimiento'],tipo_tarjeta=request.POST['form2-tipo_tarjeta'],numero_tarjeta=request.POST['form2-numero_tarjeta'],cvv=request.POST['form2-cvv'],rol='a')
                        perfil.save()
                        
            except Exception as e: 
                print(e,"error")
            messages.success(request, "Franquicia registrada")
            return redirect('franquicias:registrar')
        else:
            print(str(formUsuario.errors))
            print(str(formUserDjango.errors))
            print(str(formUserDjango.errors))
            messages.error(request, "Por favor verificar los campos en rojo")
    else:
        form = FranquiciaForm(prefix="form1")
        formUsuario = UsuarioForm(prefix="form2",initial={'rol': 'a'})
        formUserDjango = UserForm(prefix="form3")
    context = {
        'form1': form,
        'form2': formUsuario,
        'form3': formUserDjango,
        'dominios': dominios,
        'regis':True
        }
    return render(request, 'franquicias/registrar.html', context)

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

    return render(request, 'franquicias/registrar.html', {'form': form, 'dominios': dominios,'regis':False})


def check_schema(request):
    if HttpRequest.is_ajax and request.method == 'GET':        
        schema_name = request.GET.get('form1-schema_name','')       
        if schema_exists(schema_name):
            print('duplicate')  # have this for checking in console
            return HttpResponse('false')
        else:
            print("no duplicate")
            print(str(schema_name))
            return HttpResponse('true')
    else:
        return HttpResponse("Zero")


def ordenar(request):
    nombreFranquicia= request.tenant.nombre 
    franquicia = Franquicia.objects.get(schema_name=nombreFranquicia)
    context = {
        'pizzas':Pizza.objects.all(),        
        'enventas': Pizza.objects.filter(enventa=True),
        'franquicia':request,
        'colorprimario': json.loads(franquicia.configuracion)['colorprimario'],
        'colorsecundario': json.loads(franquicia.configuracion)['colorsecundario'],
        'tamanioletra': json.loads(franquicia.configuracion)['tamanioletra'],
        'tamanioletraX2': int(json.loads(franquicia.configuracion)['tamanioletra'])*2,
        'tamanioletraXpix': int(json.loads(franquicia.configuracion)['tamanioletra'])/10 +3,
        'logo':  franquicia.media,
    }
    return render(request, 'tenant/ordenar.html', context)
    
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
        
def informacion(request):
    inicio=request.tenant.fecha_corte
    dias=date.today()-inicio
    context={'dias':dias.days}
    return render(request,'franquicias/info.html',context)

def renuncia(request):
    franquicias = serializers.serialize("json", Franquicia.objects.all())
    f = {"Franquicias": franquicias}
    usuarios = serializers.serialize("json", Usuario.objects.all())
    u = {"Usuarios": usuarios}
    pizzas = serializers.serialize("json", Pizza.objects.all())
    i = {"Pizzas": pizzas}
    ingredientes = serializers.serialize("json", Ingrediente.objects.all())
    p = {"Ingredientes": ingredientes}
    data={**f,**u,**i,**p}
    return render(request,'franquicias/renuncia.html',{'data':data})

class CartAgregar(TemplateView):

    def post(self, request):
        id_producto = request.POST.get("id_producto", "")
        productico = Pizza.objects.filter(id=id_producto).values()[0]
        # detalles = Detalle(cantidad=1, precio=productico['precio'], descuento=0, producto_id=int(id_producto))
        # detalle_cart = model_to_dict(detalles)
        respuesta = {}
        if productico is not None:
            respuesta['estado'] = True
            cart = request.session.get('cart', {})
            if id_producto in cart:
                respuesta['estado'] = False
                respuesta['mensaje'] = "Producto ya añadido"
                return JsonResponse(respuesta)
            else:
                cart[''+id_producto] = productico
                request.session['cart'] = cart
                respuesta['cantidad'] = len(cart)
                respuesta['mensaje'] = "Producto añadido"
                return JsonResponse(respuesta)
        else:
            respuesta['estado'] = False
            respuesta['mensaje'] = "El producto no existe"
            return JsonResponse(respuesta)

class CartListar(TemplateView):
    template_name = "tenant/carrito_lista.html"    
    
    def get_context_data(self, **kwargs):
        context = super(CartListar, self).get_context_data(**kwargs)
        nombreFranquicia= self.request.tenant.nombre 
        franquicia = Franquicia.objects.get(schema_name=nombreFranquicia)
        context['franquicia']=self.request
        context['colorprimario'] = json.loads(franquicia.configuracion)['colorprimario']
        context['colorsecundario'] = json.loads(franquicia.configuracion)['colorsecundario']
        context['tamanioletra']=json.loads(franquicia.configuracion)['tamanioletra']
        context['tamanioletraX2'] = int(json.loads(franquicia.configuracion)['tamanioletra'])*2
        context['tamanioletraXpix'] = int(json.loads(franquicia.configuracion)['tamanioletra'])/10 +3
        context['logo'] = franquicia.media
        cart = self.request.session.get('cart', {})
        context['productos'] = cart
        return context

class CartDelete(TemplateView):

    def post(self, request):
        id_producto = request.POST.get("id_producto", "")
        cart = request.session.get('cart', {})
        del cart[id_producto]
        request.session['cart'] = cart
        respuesta = {'estado': True, 'mensaje': len(cart)}
        return JsonResponse(respuesta)

    def get_success_url(self):
        return reverse_lazy('cart_listar')

class AgregarCantidadCarrito(TemplateView):

    def post(self, request):
        cantidades = request.POST.get("cantidades", "")
        detalles = []
        self.request.session['cantidades'] = cantidades
        respuesta = {'estado': True, }
        return JsonResponse(respuesta)

class CartComprar(TemplateView):
    template_name = "tenant/carrito_comprar.html"

    def get_context_data(self, **kwargs):
        context = super(CartComprar, self).get_context_data(**kwargs)
        nombreFranquicia= self.request.tenant.nombre 
        franquicia = Franquicia.objects.get(schema_name=nombreFranquicia)
        context['franquicia']=self.request
        context['colorprimario'] = json.loads(franquicia.configuracion)['colorprimario']
        context['colorsecundario'] = json.loads(franquicia.configuracion)['colorsecundario']
        context['tamanioletra']=json.loads(franquicia.configuracion)['tamanioletra']
        context['tamanioletraX2'] = int(json.loads(franquicia.configuracion)['tamanioletra'])*2
        context['tamanioletraXpix'] = int(json.loads(franquicia.configuracion)['tamanioletra'])/10 +3
        context['logo'] = franquicia.media
        cart = self.request.session.get('cart', {})
        cantidades = self.request.session.get('cantidades', {})       
        context['productos'] = cart
        context['cantidades'] = json.loads(cantidades)        

        return context

    def post(self, request):
        direccion = request.POST['datos-direccion']
        direccion_completa = ''
        if len(direccion) > 0:
            datos = json.loads(direccion)
            tamano_datos = len(datos)
            efectivo = datos[int(tamano_datos) - 2]['value']
            for x in range(1, int(tamano_datos)-2):
                direccion_completa += datos[x]['value']+' '
        usuario = request.user
        if usuario.is_authenticated():
            cliente = Usuario.objects.get(user_id=usuario.id)
            factura = Factura(direccion=direccion_completa, estado_Factura=0, efectivo=efectivo, cliente=cliente)
            factura.save()
        else:
            usuario_anonimo = User.objects.get(email="anonimo@superpizzas.com")
            cliente_anonimo = Usuario.objects.get(user_id=usuario_anonimo.id)
            factura = Factura(direccion=direccion_completa, estado_Factura=0, efectivo=efectivo, cliente=cliente_anonimo)
            factura.save()
        cantidades = self.request.session.get('cantidades', {})
        cantidades_dict = json.loads(cantidades)
        for k, v in cantidades_dict.items():
            productico = Pizza.objects.filter(id=v['id']).values()[0]
            detallito = Detalle(cantidad=v['cantidad'], precio=productico['precio'], factura=factura,
                                producto_id=v['id'])
            detallito.save()
        self.request.session['cart'] = {}
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('cart_success')

class CartSuccess(TemplateView):
    template_name = "tenant/carrito_success.html"

    def get_context_data(self, **kwargs):
        context = super(CartSuccess, self).get_context_data(**kwargs)
        context['configuracion'] = obtener_configuracion()
        context['datos_franquicia'] = obtener_datos_franquicia()
        namespace = self.request.resolver_match.namespace
        context['namespace'] = namespace
        context['extend_name'] = extend_name(namespace)
        return context