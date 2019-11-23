import datetime
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.http import HttpResponse
from apps.usuarios.forms import UsuarioForm, UserForm
from apps.pizzas.forms import FacturaForm
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
from apps.usuarios.forms import UserAuthenticationForm
from django.contrib.auth import authenticate
from reportlab.pdfgen import canvas
from django.views.generic import View
from io import BytesIO




def home(request):
    if(request.tenant.working==True):
        #Si usario es anonimo? 
        if request.user.is_anonymous:
            return redirect('/')
        #Validacion del Formulario a traves del metodo POST
        else:
            id_usuario = request.user.id

            perfil = Usuario.objects.get(user=id_usuario)

            if perfil.rol != 'c':
                return render(request, 'base.html', {})
            else:
                return redirect('/login')
    else:
        return render(request,"404.html",{})
    

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
                        
                          # Cliente anonimo 

                        user_anonimo = User(username='anonimo@superpizzas.com',password="V7IyWywC9JZyno", email='anonimo@superpizzas.com', first_name='anonimo', last_name='anonimo')
                                                                        
                        user_anonimo.save()

                        assign_role(user_anonimo,'cliente')

                        cliente_anonimo = Usuario(user=user_anonimo,cc=0000000000,telefono=0000000000,pais='CO',nombre_banco='bancolombia',fecha_vencimiento='2019-11-21',tipo_tarjeta='visa',numero_tarjeta=000000000000000,cvv=000,rol='c')

                        cliente_anonimo.save()
                      

            except Exception as e: 
                print(e,"error")
            context={
                'nombre': form.data.get('form1-nombre'),
                'schema': form.data.get('form1-schema_name'),
            }
            return render(request,'landingpage/comprado.html',context)
        else:
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
    if(request.tenant.working==True):
        franquicia = Franquicia.objects.get(schema_name=request.tenant.schema_name)
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
    else:
        return render(request,"404.html",{})

def modificar_franquicia(request, id_franquicia):
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
            return HttpResponse('false')
        else:
            return HttpResponse('true')
    else:
        return HttpResponse("Zero")


def ordenar(request):
    if(request.tenant.working==True):
        franquicia = Franquicia.objects.get(schema_name=request.tenant.schema_name)
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
    else:
        return render(request,"404.html",{})
    
def configuraciones(request):
    if(request.user.usuario.rol=='a' and request.tenant.working==True and request.tenant.tipo.nombre=='premium'):
        if(request.tenant.tipo.nombre=="premium"):
            datosfran = Franquicia.objects.get(schema_name=request.tenant.schema_name)
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

                datosfran = Franquicia.objects.get(schema_name=request.tenant.schema_name)
                contexto = {'franquicia': datosfran, 
                'colorprimario': json.loads(datosfran.configuracion)['colorprimario'],
                'colorsecundario': json.loads(datosfran.configuracion)['colorsecundario'],
                'logo':  datosfran.media,
                'tamanioletra': json.loads(datosfran.configuracion)['tamanioletra']
                }
            return render(request,'franquicias/configuraciones.html', contexto)
        else:
            return redirect('/admin')
    else:
        return render(request,"404.html",{})

def informacion(request):
    if(request.user.usuario.rol=='a' and request.tenant.working==True):
        inicio=request.tenant.fecha_corte
        dias=date.today()-inicio
        if request.method == 'POST':
            formulario = UserAuthenticationForm(request.POST)
            if formulario.is_valid:
                username = request.POST['username']
                password = request.POST['password']
                acceso_user = authenticate(username = username, password = password)
                user = User.objects.get(username=acceso_user)
                perfil = Usuario.objects.get(user=user)
                if acceso_user is not None and perfil.rol== 'a':
                    if acceso_user.is_active:
                        return renuncia(request)
                    else:
                        messages.add_message(request, messages.INFO, 'Error en usuario y contraseña')
                else:
                    messages.add_message(request, messages.INFO, 'Error en usuario y contraseña')
            else:
                messages.add_message(request, messages.INFO, 'Error en usuario y contraseña')
        else:
            formulario = UserAuthenticationForm()

        context={'dias':dias.days,'formulario':formulario}
        return render(request,'franquicias/info.html',context)
    else:
        return render(request,"404.html",{})

def renuncia(request):
    if(request.tenant.working==True):
        franquiciafields={"nombre":request.tenant.nombre,"dominio":request.tenant.schema_name,"tipo":request.tenant.tipo.nombre}
        franquicia={"model":"franquicias.franquicia","pk":request.tenant.id,"fields":franquiciafields}
        usuarios = serializers.serialize("json", Usuario.objects.all())
        ingredientes = serializers.serialize("json", Ingrediente.objects.all())
        pizzas = serializers.serialize("json", Pizza.objects.all())
        facturas = serializers.serialize("json", Factura.objects.all())
        detalles = serializers.serialize("json", Detalle.objects.all())
        context={'f':json.dumps(franquicia),'u':usuarios,'i':ingredientes,'p':pizzas,'fc':facturas,'dt':detalles}
        Franquicia.objects.filter(pk=request.tenant.id).update(working=False)
        return render(request,'tenant/renuncia.html',context)
    else:
        return render(request,"404.html",{})

class CartAgregar(TemplateView):

    def post(self, request):
        if(request.tenant.working==True):
            id_producto = request.POST.get("id_producto", "")
            producto_item = Pizza.objects.filter(id=id_producto).values()[0]       
            respuesta = {}        
            if producto_item is not None:
                respuesta['estado'] = True
                cart = request.session.get('cart', {})
                if id_producto in cart:
                    respuesta['estado'] = False
                    respuesta['mensaje'] = "La pizza ya está añadida en el carrito de compras "                            
                    return JsonResponse(respuesta)
                else:
                    cart[''+id_producto] = producto_item
                    request.session['cart'] = cart
                    respuesta['cantidad'] = len(cart)
                    respuesta['mensaje'] = "Has añadido la pizza al carrito de compras"                              
                    return JsonResponse(respuesta)
            else:
                respuesta['estado'] = False
                respuesta['mensaje'] = "El producto no existe"
                return JsonResponse(respuesta)
        else:
            return render(request,"404.html",{})

class CartListar(TemplateView):
    template_name = "tenant/carrito_lista.html"    
    
    def get_context_data(self, **kwargs):
        if(self.request.tenant.working==True):
            context = super(CartListar, self).get_context_data(**kwargs)
            franquicia = Franquicia.objects.get(schema_name=self.request.tenant.schema_name)
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
        else:
            return render(self.request,"404.html",{})

class CartDelete(TemplateView):

    def post(self, request):
        if(request.tenant.working==True):
            id_producto = request.POST.get("id_producto", "")
            cart = request.session.get('cart', {})
            del cart[id_producto]
            request.session['cart'] = cart
            respuesta = {'estado': True, 'mensaje': len(cart)}
            return JsonResponse(respuesta)
        else:
            return render(request,"404.html",{})

    def get_success_url(self):
        return reverse_lazy('cart_listar')

class AgregarCantidadCarrito(TemplateView):

    def post(self, request):
        if(request.tenant.working==True):
            cantidades = request.POST.get("cantidades", "")
            detalles = []
            self.request.session['cantidades'] = cantidades
            respuesta = {'estado': True, }
            return JsonResponse(respuesta)
        else:
            return render(request,"404.html",{})

class CartComprar(TemplateView):
    template_name = "tenant/carrito_comprar.html"
    
    def get_context_data(self, **kwargs):
        if(self.request.tenant.working==True):
            context = super(CartComprar, self).get_context_data(**kwargs)
            franquicia = Franquicia.objects.get(schema_name=self.request.tenant.schema_name)
            form = UsuarioForm(self.request.POST or None,prefix="form2") 
            form_factura= FacturaForm(self.request.POST or None)
            admin_franquicia = Usuario.objects.get(user_id=1)
            cliente=None
            customer = self.request.user        
            if customer.is_authenticated:                
                cliente = Usuario.objects.get(user_id=customer.id)            
            context["form"] = form_factura
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
            context['cliente']=cliente 
            context["form2"] = form
            context['admin_franquicia']=admin_franquicia

            return context
        else:
            return render(self.request,"404.html",{})

    def post(self, request):
        if(request.tenant.working==True):
            direccion = request.POST['form2-direccion']
            ciudad= request.POST['ciudad']            
            customer = request.user        
            if customer.is_authenticated:
                cliente = Usuario.objects.get(user_id=customer.id)
                factura = Factura(direccion=direccion, ciudad=ciudad, cliente=cliente)
                factura.save()
            else:
                if not User.objects.filter(email="anonimo@superpizzas.com").exists():
                    user_anonimo = User(username='anonimo@superpizzas.com',password="V7IyWywC9JZyno", email='anonimo@superpizzas.com', first_name='anonimo', last_name='anonimo')
                    user_anonimo.save()
                    assign_role(user_anonimo,'cliente')
                    cliente_anonimo = Usuario(user=user_anonimo,cc=0000000000,telefono=0000000000,pais='CO',nombre_banco='bancolombia',fecha_vencimiento='2019-11-21',tipo_tarjeta='visa',numero_tarjeta=000000000000000,cvv=000,rol='c')
                    cliente_anonimo.save()

                usuario_anonimo = User.objects.get(email="anonimo@superpizzas.com")
                cliente_anonimo = Usuario.objects.get(user_id=usuario_anonimo.id)
                factura = Factura(direccion=direccion, ciudad=ciudad, cliente=cliente_anonimo)
                factura.save()
            cantidades = self.request.session.get('cantidades', {})
            cantidades_dict = json.loads(cantidades)
            for k, v in cantidades_dict.items():
                producto_item = Pizza.objects.filter(id=v['id']).values()[0]
                detalle_item = Detalle(cantidad=v['cantidad'], precio=producto_item['valor'], factura=factura,
                                    producto_id=v['id'])
                detalle_item.save()
            self.request.session['cart'] = {}
            #return HttpResponseRedirect(self.get_success_url())
            return HttpResponseRedirect('/compra_exitosa?id='+str(factura.id))
        else:
            return render(request,"404.html",{})



class CartSuccess(TemplateView):
    template_name = "tenant/carrito_success.html"

    def get_context_data(self, **kwargs):
        if(self.request.tenant.working==True):
            context = super(CartSuccess, self).get_context_data(**kwargs)
            franquicia = Franquicia.objects.get(schema_name=self.request.tenant.schema_name)
            context['franquicia']=self.request
            context['colorprimario'] = json.loads(franquicia.configuracion)['colorprimario']
            context['colorsecundario'] = json.loads(franquicia.configuracion)['colorsecundario']
            context['tamanioletra']=json.loads(franquicia.configuracion)['tamanioletra']
            context['tamanioletraX2'] = int(json.loads(franquicia.configuracion)['tamanioletra'])*2
            context['tamanioletraXpix'] = int(json.loads(franquicia.configuracion)['tamanioletra'])/10 +3
            context['logo'] = franquicia.media
            context['id_factura'] = self.request.GET['id']

            return context
        else:
            return render(self.request,"404.html",{})

def factura_PDF(request, id_factura=None):
    
    #Indicamos el tipo de contenido a devolver, en este caso un pdf
    response = HttpResponse(content_type='application/pdf')
    #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
    buffer = BytesIO()
    #Canvas nos permite hacer el reporte con coordenadas X y Y
    pdf = canvas.Canvas(buffer)
    pdf.setTitle("Factura de Venta")
    pdf.setPageSize((200, 300))
    #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.

    archivo_imagen = settings.MEDIA_ROOT+'/images/favicon.png'
    pdf.drawImage(archivo_imagen, 25, 240, 50, 50,preserveAspectRatio=True)
    
    pdf.setFont("Helvetica", 8)
    
    pdf.drawString(80, 280, request.tenant.nombre)
    pdf.drawString(80, 270, u"FACTURA DE VENTA")
    pdf.setFont("Helvetica", 7)
    pdf.drawString(80, 260, id_factura)
    pdf.drawString(80, 250, str(datetime.datetime.now().strftime("%Y-%m-%d")))

    factura = Factura.objects.get(id=id_factura)
    detalles = Detalle.objects.filter(factura=factura)

    
    pdf.drawString(25, 230, "---------------------------------------------------------------")
    pdf.setFont("Helvetica", 8)
    pdf.drawString(25, 220, "Nombre:")
    if factura.cliente.user.first_name == "anonimo":
        pdf.drawString(70, 220, "No disponible")
    else:
        pdf.drawString(70, 220, factura.cliente.user.first_name+" "+factura.cliente.user.last_name)

    pdf.drawString(25, 210, "Email:")
    if factura.cliente.user.first_name == "anonimo":
        pdf.drawString(70, 210, "No disponible")
    else:
        pdf.drawString(70, 210, factura.cliente.user.username)
    pdf.drawString(25, 200, "Dirección:")
    pdf.drawString(70, 200, factura.direccion)
    pdf.setFont("Helvetica", 7)
    pdf.drawString(25, 190, "---------------------------------------------------------------")
    pdf.setFont("Helvetica", 8)
    pdf.drawString(25, 180, "Resumen de Venta:")
    pdf.setFont("Helvetica", 6)
    pdf.drawString(25, 170, "Cant")
    pdf.drawString(50, 170, "Descripción")
    pdf.drawString(150, 170, "Valor")
    total = 0
    line = 160
    for detalle in detalles:

        pdf.drawString(25, line, str(detalle.cantidad))
        pdf.drawString(50, line, detalle.producto.nombre)
        valor = int(detalle.cantidad)*int(detalle.precio)
        pdf.drawString(150, line, "$ "+str(valor))
        line -= 10
        total += valor

    pdf.setFont("Helvetica", 8)
    pdf.drawString(120, line-10, "Total")
    pdf.drawString(150, line-10, "$ "+str(total))

    pdf.setFont("Helvetica", 5)
    pdf.drawString(25, 25, "Fecha de orden: ")
    pdf.drawString(70, 25, str(factura.fecha_creacion))

    pdf.showPage()
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

def vender(request):
    if(request.user.usuario.rol=='v' and request.tenant.working==True):
        franquicia = Franquicia.objects.get(schema_name=request.tenant.schema_name)
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
        return render(request, 'tenant/vender.html', context)
    else:
        return render(request,"404.html",{})

class VentaCantidades(TemplateView):

    def post(self, request):
        if(request.tenant.working==True):
            cantidades = request.POST.get("cantidades_venta", "")
            detalles = []
            self.request.session['cantidades_venta'] = cantidades
            respuesta = {'estado': True, }
            return JsonResponse(respuesta)
        else:
            return render(request,"404.html",{})

def VenderPago(request):
    if(request.user.usuario.rol=='v' and request.tenant.working==True):
        franquicia = Franquicia.objects.get(schema_name=request.tenant.schema_name)
        cantidades = request.session.get('cantidades_venta', {})
        cantidades_dict = json.loads(cantidades)  
        cliente=None
        customer = request.user    
        id=[]     
        if customer.is_authenticated: 
            cliente = Usuario.objects.get(user_id=customer.id)                
        for k, v in cantidades_dict.items():
            id.append(v['id']) 
        pizza_item = Pizza.objects.filter(id__in=id)           
        if request.method == 'POST': 
            customer = request.user        
            if customer.is_authenticated:
                cliente = Usuario.objects.get(user_id=customer.id)
                factura = Factura(direccion='local', ciudad='local', cliente=cliente)
                factura.save()                               
            for k, v in cantidades_dict.items():
                print("for")
                producto_item = Pizza.objects.filter(id=v['id']).values()[0] 
                detalle_item = Detalle(cantidad=v['cantidad'], precio=producto_item['valor'], factura=factura,
                                    producto_id=v['id'])
                detalle_item.save()
            request.session['cantidades_venta'] = {}
            messages.success(request, 'Venta realizada')
            return redirect('vender')
        else:
            context = {
                'productos': pizza_item ,
                'cantidades':cantidades_dict,
                'franquicia':request,
                'colorprimario': json.loads(franquicia.configuracion)['colorprimario'],
                'colorsecundario': json.loads(franquicia.configuracion)['colorsecundario'],
                'tamanioletra': json.loads(franquicia.configuracion)['tamanioletra'],
                'tamanioletraX2': int(json.loads(franquicia.configuracion)['tamanioletra'])*2,
                'tamanioletraXpix': int(json.loads(franquicia.configuracion)['tamanioletra'])/10 +3,
                'logo':  franquicia.media,               
            }
            return render(request, 'tenant/vender_pago.html', context)
    else:
        return render(request,"404.html",{})



def reportes(request):
    if(request.user.usuario.rol=='a' and request.tenant.working==True and request.tenant.tipo.nombre=='premium'):
        vmeses=[0,0,0,0,0,0,0,0,0,0,0,0]
        pizza1="Hawa"
        pizza2="Poll"
        pizza3="Otr"
        for factura in Factura.objects.all():
            vmeses[factura.fecha_creacion.month-1]+=1
        contexto={'vene':vmeses[0],'vfeb':vmeses[1],'vmar':vmeses[2],'vabr':vmeses[3],'vmay':vmeses[4],'vjun':vmeses[5],'vjul':vmeses[6],'vago':vmeses[7],'vsep':vmeses[8],'voct':vmeses[9],'vnov':vmeses[10],'vdic':vmeses[11],'pizza1':pizza1,'pizza2':pizza2,'pizza3':pizza3,}
        return render(request,'franquicias/graficos.html', contexto)
    else:
        return render(request,"404.html",{})
