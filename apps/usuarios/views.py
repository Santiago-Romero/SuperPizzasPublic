from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import Usuario
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect 



def gestionar_usuario(request, id_usuario=None):
    
    usuarios = User.objects.all()
    usuario = None
    
    if request.method == 'POST':
        
        if request.POST['user']=='':
            form = UsuarioForm2(request.POST)
            formUserDjango = UserForm(request.POST)

            if formUserDjango.is_valid():

                print(request.POST)
                
                usuario = formUserDjango.save(commit=False)
                        
                usuario = User(username=request.POST['username'], email=request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                        
                usuario.set_password(request.POST['password1'])
                        
                usuario.save()

                #CREACION DEL USUARIO - INFORMACIÓN ADICIONAL

                perfil = Usuario(user=usuario,cc=request.POST['cc'],telefono=request.POST['telefono'],pais=request.POST['pais'],nombre_banco=request.POST['nombre_banco'],fecha_vencimiento=request.POST['fecha_vencimiento'],tipo_tarjeta=request.POST['tipo_tarjeta'],numero_tarjeta=request.POST['numero_tarjeta'],cvv=request.POST['cvv'],rol=request.POST['rol-user'])

                perfil.save()

            else:

                print(str(form.errors))
                print(str(formUserDjango.errors))

        else:
            usuario = get_object_or_404(Usuario, cc=request.POST['cc'])
            user = User.objects.get(pk=usuario.user.id)
            form = UsuarioForm2(request.POST, instance=usuario)
            form2 = UpdateUser(data=request.POST, instance=user)
            print(request.POST)

            if form.is_valid():
                form.save()
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.email = request.POST['email']
                user.save()
                messages.success(request, 'Usuario actualizado correctamente')
                form = UsuarioForm2()
                form2 = UserForm()
                usuario = None
                
                return redirect('usuarios:registrar')
        
            else:
                messages.error(request, 'Por favor verificar los campos en rojo')
                print(str(form.errors))
                print(str(form2.errors))

    if id_usuario:
        usuario = get_object_or_404(Usuario, id=id_usuario)
        user = User.objects.get(pk=usuario.user.id)
        form = UsuarioForm2(instance=usuario)
        form.fields['rol'].initial = [usuario.rol]
        form2 = UpdateUser(instance=user)
        flag = 0
        print(request.GET)
    else:
        form = UsuarioForm2()    
        form2 = UserForm()
        flag = 1


    return render(request, 'usuarios/gestionar_usuario.html', {'form': form, 'usuario': usuario, 'usuarios': usuarios, 'form2':form2,'flag':flag})

def gestionar_cliente(request, id_cliente=None):
    """
    Permite la creación y modificación de usuarios
    :param request:
    :param id_usuario:
    :return:
    """
    if id_cliente:
        usuario = get_object_or_404(Usuario, id=id_cliente)
    else:
        usuario = None
    form = UsuarioForm(instance=usuario)
    usuarios = Usuario.objects.all()
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado correctamente')
            return redirect('usuarios:registrarcliente')
        else:
            messages.error(request, 'Por favor verificar los campos en rojo')
    return render(request, 'usuarios/registro_cliente.html', {'form': form, 'UserForm': UserForm, 'usuario': usuario, 'usuarios': usuarios})


def eliminar_usuario(request, id_usuario):
    
    usuario = get_object_or_404(Usuario, id=id_usuario)

    if usuario != None:
        user = User.objects.get(pk=usuario.user.id)
        usuario.delete()
        user.delete()
        messages.success(request, 'Usuario eliminado correctamente')
        return redirect('usuarios:registrar')
    else:
        messages.warning(request, 'Usuario no encontrado')
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
            print(acceso_user)
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
                messages.warning(request, 'Por favor revisa tu usuario o password')
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

