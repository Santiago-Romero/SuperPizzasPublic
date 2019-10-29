from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import Usuario
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect 


def gestionar_usuario(request, id_usuario=None):
    """
    Permite la creación y modificación de usuarios
    :param request:
    :param id_usuario:
    :return:
    """
    if id_usuario:
        usuario = get_object_or_404(Usuario, id=id_usuario)
    else:
        usuario = None
    form = UsuarioForm(instance=usuario)
    usuarios = Usuario.objects.all()
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente')
            return redirect('usuarios:registrar')
        else:
            messages.error(request, 'Por favor verificar los campos en rojo')
    return render(request, 'usuarios/gestionar_usuario.html', {'form': form, 'usuario': usuario, 'usuarios': usuarios})


def eliminar_usuario(request, id_usuario):
    """
    Permite la eliminación de usuarios
    :param request:
    :param id_usuario:
    :return:
    """
    usuario = get_object_or_404(Usuario, id=id_usuario)
    usuario.delete()
    messages.success(request, 'Usuario eliminado correctamente')

    return redirect('usuarios:registrar')


@csrf_protect
def inicio_sesion(request):

    #Si usario no es anonimo? (ya esta log)
    if not request.user.is_anonymous:
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
                messages.add_message(request, messages.INFO, 'Por favor revisa tu usuario o password')
        else:
            messages.add_message(request, messages.INFO, 'Error')
    else:
        formulario = UserAuthenticationForm()
        
    contexto = {
        'formulario': formulario
    }

    return render(request,  'tenant/login.html', context=contexto) 



@csrf_protect
def inicio_sesion_admin(request):

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
                messages.add_message(request, messages.INFO, 'Por favor revisa tu usuario o password')
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