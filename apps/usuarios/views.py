from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *


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
