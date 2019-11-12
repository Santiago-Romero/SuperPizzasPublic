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
                        
                usuario = User(username=request.POST['email'], email=request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                        
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
                user.username = request.POST['email']
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
    if request.method == 'POST':
        form = UsuarioForm(request.POST,prefix="form2",initial={'rol': 'c'})
        formUserDjango = UserForm(request.POST,prefix="form3")
        
        if formUserDjango.is_valid():

            usuario = formUserDjango.save(commit=False)

            usuario = User(username=request.POST['form3-username'], email=request.POST['form3-email'], first_name=request.POST['form3-first_name'], last_name=request.POST['form3-last_name'])
                        
            usuario.set_password(request.POST['form3-password1'])

            usuario.save()

            #CREACION DEL USUARIO - INFORMACIÓN ADICIONAL

            perfil = Usuario(user=usuario,cc=request.POST['form2-cc'],telefono=request.POST['form2-telefono'],pais=request.POST['form2-pais'],nombre_banco=request.POST['form2-nombre_banco'],fecha_vencimiento=request.POST['form2-fecha_vencimiento'],tipo_tarjeta=request.POST['form2-tipo_tarjeta'],numero_tarjeta=request.POST['form2-numero_tarjeta'],cvv=request.POST['form2-cvv'],rol='a')

            perfil.save()   

            messages.success(request, 'Cliente registrado correctamente')
            return redirect('login')
        else:
            messages.error(request, 'Por favor verificar los campos en rojo')
            print(str(form.errors))
            print(str(formUserDjango.errors))
    else:
        form = UsuarioForm(prefix="form2",initial={'rol': 'a'})
        formUserDjango = UserForm(prefix="form3")        
    return render(request, 'usuarios/registro_cliente.html', {'form2': form, 'form3': formUserDjango})


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


#Retorna 1 si es anonimo / 2 si es admin / 3 si es digitador / 4 si es vendedor / 5 si es cliente / 6 error
def get_role_user(request):
    if request.user.is_anonymous:
        return 1;
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
