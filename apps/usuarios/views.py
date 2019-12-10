from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect 
from rolepermissions.roles import assign_role
from django.http import HttpResponse
from django.http import HttpRequest
from apps.franquicias.models import Franquicia
import json

def gestionar_usuario(request, id_usuario=None):
    if request.user.is_anonymous:
        return render(request,"404.html",{})
    else:
        if(request.user.usuario.rol=='a' and request.tenant.working==True):
            usuarios = User.objects.all()
            usuario = None
            if request.method == 'POST':
                print(" ESTÁ POST -------------------")
                if request.POST['user']=='':
                    form = UsuarioForm2(request.POST)
                    formUserDjango = UserForm(request.POST)

                    if formUserDjango.is_valid():
                        if not User.objects.filter(email=request.POST['email']):
                            usuario = formUserDjango.save(commit=False)
                            usuario = User(username=request.POST['email'], email=request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                            usuario.set_password(request.POST['password1'])
                            usuario.save()
                            perfil = Usuario(user=usuario,cc=request.POST['cc'],telefono=request.POST['telefono'],nombre_banco=request.POST['nombre_banco'],fecha_vencimiento=request.POST['fecha_vencimiento'],tipo_tarjeta=request.POST['tipo_tarjeta'],numero_tarjeta=request.POST['numero_tarjeta'],cvv=request.POST['cvv'],rol=request.POST['rol'])
                            perfil.save()
                        else:
                            messages.error(request, 'Ya existe ese usuario con ese correo')
                    else:
                        messages.error(request,'Por favor verificar los campos, recuerda poner una contraseña segura')

                else:
                    usuario = get_object_or_404(Usuario, id=id_usuario)
                    user = User.objects.get(pk=usuario.user.id)
                    form = UsuarioForm2(request.POST, instance=usuario)
                    form2 = UpdateUser(data=request.POST, instance=user)

                    if form.is_valid():
                        if(not User.objects.filter(email=request.POST['email']) or user.email==request.POST['email']):
                            form.save()
                            user.first_name = request.POST['first_name']
                            user.last_name = request.POST['last_name']
                            user.email = request.POST['email']
                            user.username = request.POST['email']
                            user.set_password(request.POST['password1'])
                            user.save()
                            messages.success(request, 'Usuario actualizado correctamente')
                            form = UsuarioForm2()
                            form2 = UserForm()
                            usuario = None
                            return redirect('usuarios:registrar')
                        else:
                            messages.error(request, 'Ya existe ese usuario con ese correo')
                
                    else:
                        messages.error(request, 'Por favor verificar los campos en rojo')
            print(" WTFFFFFFFFFFFFFFFF -------------------", id_usuario)
            if id_usuario:
                usuario = get_object_or_404(Usuario, id=id_usuario)
                user = User.objects.get(pk=usuario.user.id)
                form = UsuarioForm2(instance=usuario)
                form.fields['rol'].initial = [usuario.rol]
                form2 = UpdateUser(instance=user)
                flag = 0
            else:
                form = UsuarioForm2()    
                form2 = UserForm()
                flag = 1


            return render(request, 'usuarios/gestionar_usuario.html', {'form': form, 'usuario': usuario, 'usuarios': usuarios, 'form2':form2,'flag':flag})
        else:
            return render(request,"404.html",{})

def gestionar_cliente(request):
    if(request.tenant.working==True):
        if request.method == 'POST':
            form = UsuarioForm(request.POST,prefix="form2",initial={'rol': 'c'})
            formUserDjango = UserForm(request.POST,prefix="form3")
            if formUserDjango.is_valid():
                usuario = formUserDjango.save(commit=False)
                usuario = User(username=request.POST['form3-email'], email=request.POST['form3-email'], first_name=request.POST['form3-first_name'], last_name=request.POST['form3-last_name'])
                usuario.set_password(request.POST['form3-password1'])
                usuario.save()            
                perfil = Usuario(user=usuario,cc=request.POST['form2-cc'],telefono=request.POST['form2-telefono'],direccion=request.POST['form2-direccion'],nombre_banco=request.POST['form2-nombre_banco'],fecha_vencimiento=request.POST['form2-fecha_vencimiento'],tipo_tarjeta=request.POST['form2-tipo_tarjeta'],numero_tarjeta=request.POST['form2-numero_tarjeta'],cvv=request.POST['form2-cvv'],rol='c')
                perfil.save()
                messages.success(request, 'Cliente registrado correctamente')
                return redirect('login')
            else:
                messages.error(request,'Por favor verificar los campos, recuerda poner una contraseña segura')
        else:
            form = UsuarioForm(prefix="form2",initial={'rol': 'c'})
            formUserDjango = UserForm(prefix="form3")
        datosfran = Franquicia.objects.get(schema_name=request.tenant.schema_name)
        return render(request, 'usuarios/registro_cliente.html', {'form2': form, 'form3': formUserDjango, 'colorprimario': json.loads(datosfran.configuracion)['colorprimario'], 'colorsecundario': json.loads(datosfran.configuracion)['colorsecundario']})
    else:
        return render(request,"404.html",{})

def eliminar_usuario(request, id_usuario):
    if request.user.is_anonymous:
        return render(request,"404.html",{})
    else:
        if(request.user.usuario.rol=='a' and request.tenant.working==True):
            usuario = get_object_or_404(Usuario, id=id_usuario)

            if (usuario != None):
                if(id_usuario != 1 and id_usuario != 2):
                    user = User.objects.get(pk=usuario.user.id)
                    usuario.delete()
                    user.delete()
                    messages.success(request, 'Usuario eliminado correctamente')
                    return redirect('usuarios:registrar')
                else:
                    messages.error(request, 'No puedes elimiar este usuario')
                return redirect('usuarios:registrar')
            else:
                messages.warning(request, 'Usuario no encontrado')
                return redirect('usuarios:registrar')
        else:
            return render(request,"404.html",{})

@csrf_protect
def inicio_sesion(request):
    if(request.tenant.working==True):
        #Si usario no es anonimo? (ya esta log)
        if not request.user.is_anonymous:
            
            role = get_role_user(request)

            if role == 5:

                return HttpResponseRedirect('/')

            else:

                return HttpResponseRedirect('/admin')

        #Validacion del Formulario a traves del metodo POST
        if request.method == 'POST':
            formulario = UserAuthenticationForm(request.POST)

            if formulario.is_valid:
                username = request.POST['username']
                password = request.POST['password']
                acceso_user = authenticate(username = username, password = password)
                # Si el log fue existoso?
                if acceso_user is not None:
                    #si el usuario esta activo
                    if acceso_user.is_active:
                        #Login
                        login(request,acceso_user)

                        user = User.objects.get(username=acceso_user)
                        perfil = Usuario.objects.get(user=user)


                        if perfil.rol == 'c':
                            #Redireccion al origen
                            return redirect('/')
                        else:
                            #Redireccion al origen
                            return redirect('/admin')
                    else:
                        messages.add_message(request, messages.INFO, 'Error')
                else:
                    messages.add_message(request, messages.INFO, 'Por favor revisa tu usuario o contraseña')
            else:
                messages.add_message(request, messages.INFO, 'Error')
        else:
            formulario = UserAuthenticationForm()

        datosfran = Franquicia.objects.get(schema_name=request.tenant.schema_name)
        contexto = {
            'formulario': formulario,
            'colorprimario': json.loads(datosfran.configuracion)['colorprimario'],
            'colorsecundario': json.loads(datosfran.configuracion)['colorsecundario'],
        }

        return render(request,  'tenant/login.html', context=contexto)
    else:
        return render(request,"404.html",{})



@csrf_protect
def inicio_sesion_admin(request,id=None):

    #Si usario no es anonimo? (ya esta log)
    if request.user.is_superuser:
        #Redireccion a Raiz
        return HttpResponseRedirect('/admin')
    #Validacion del Formulario a traves del metodo POST
    if request.method == 'POST':

        formulario = UserAuthenticationForm(request.POST)

        if formulario.is_valid:
            
            username = request.POST['username']
            password = request.POST['password']
            acceso_user = authenticate(username = username, password = password)
            # Si el log fue existoso?
            if acceso_user is not None:
                #si el usuario esta activo
                if acceso_user.is_active:
                    #Login
                    login(request,acceso_user)
                    #Redireccion al origen
                    return redirect('/admin')
                else:
                    messages.add_message(request, messages.INFO, 'Error')
            else:
                messages.warning(request, 'Por favor revisa tu usuario o contraseña')
                return render(request,  'landingpage/login.html', {'formulario':formulario}) 
                #messages.add_message(request, messages.INFO, 'Por favor revisa tu usuario o password')
        else:
            messages.add_message(request, messages.INFO, 'Error')
    else:

        formulario = UserAuthenticationForm()
        
        contexto = {
        'formulario': formulario
        }

        return render(request,  'landingpage/login.html', context=contexto) 



def cerrar_sesion(request):
    if not request.user.is_anonymous:
        logout(request)
        return redirect('/login')
    else:
        return redirect('/admin')

def check_email(request):
    if(request.tenant.working==True):
        if HttpRequest.is_ajax and request.method == 'GET':        
            email = request.GET.get('form3-email','') 
            if User.objects.filter(email=email).exists():
                return HttpResponse('false')
            else:
                return HttpResponse('true')
        else:
            return HttpResponse("Zero")
    else:
        return render(request,"404.html",{})

def mostrarclientes(request):
    if request.user.is_anonymous:
        return render(request,"404.html",{})
    else:
        if(request.user.usuario.rol=='a' and request.tenant.working==True):
            context={'usuarios':User.objects.all()}
            return render(request,'usuarios/clientes.html',context)
        else:
            return render(request,"404.html",{})

#Retorna 1 si es anonimo / 2 si es admin / 3 si es digitador / 4 si es vendedor / 5 si es cliente / 6 error
def get_role_user(request):
    if request.user.is_anonymous:
        return 1
    else:
        usuario = request.user
        user = User.objects.get(pk=usuario.id)
        perfil = Usuario.objects.get(user=user)

        if perfil.rol == 'a':
            return 2
        elif perfil.rol == 'd':
            return 3
        elif perfil.rol == 'v':
            return 4
        elif perfil.rol == 'c':
            return 5
        else:
            return 6

def modificarcliente(request):
    if request.user.is_anonymous:
        return render(request,"404.html",{})
    else:
        if(request.user.usuario.rol=='c' and request.tenant.working==True):
            if request.method == 'POST':
                usuario = get_object_or_404(Usuario, id=request.user.usuario.id)
                user = User.objects.get(pk=usuario.user.id)
                form = UsuarioForm(request.POST, instance=usuario)
                form2 = UpdateUser(data=request.POST, instance=user)
                if form.is_valid():
                    if(not User.objects.filter(email=request.POST['email']) or user.email==request.POST['email']):
                        form.save()
                        user.first_name = request.POST['first_name']
                        user.last_name = request.POST['last_name']
                        user.email = request.POST['email']
                        user.username = request.POST['email']
                        user.set_password(request.POST['password1'])
                        user.save()
                        messages.success(request, 'Usuario actualizado correctamente')
                        return redirect('/')
                    else:
                        messages.error(request, 'El correo ya pertenece a otro usuario')
                else:
                    messages.error(request,'Por favor verificar los campos, recuerda poner una contraseña segura')
            usuario = get_object_or_404(Usuario, id=request.user.usuario.id)
            user = User.objects.get(pk=usuario.user.id)
            form = UsuarioForm(instance=usuario)
            form.fields['rol'].initial = [usuario.rol]
            form2 = UpdateUser(instance=user)
            datosfran = Franquicia.objects.get(schema_name=request.tenant.schema_name)
            return render(request, 'usuarios/modificar_cliente.html', {'form': form, 'usuario': usuario,'form2':form2, 'colorprimario': json.loads(datosfran.configuracion)['colorprimario'], 'colorsecundario': json.loads(datosfran.configuracion)['colorsecundario']})
        else:
            return render(request,"404.html",{})
