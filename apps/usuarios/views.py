from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import Usuario


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

def login_view(request):
    form=LoginForm(request.POST or None)
    context={
        "form":form,
        "mensaje":''
        }
    if form.is_valid():
        nickname=form.cleaned_data.get("nickname")
        password=form.cleaned_data.get("password")    
        user_exists = Usuario.objects.filter(nickname=nickname)
        print(user_exists)
        if user_exists:
            db_password = str(user_exists[0].password)            
            if password==db_password:
                messages.info(request, "Bienvenido, "+nickname)
                return redirect('/admin')
            else:
                context["mensaje"]='Contraseña incorrecta'
                return render(request,"tenant/login.html",context)
        else:
            context["mensaje"]='Nickname o contraseña incorrectos'
            return render(request,"tenant/login.html",context)
        return redirect('/login')
    context["mensaje"]=''    
    return render(request,"tenant/login.html",context)