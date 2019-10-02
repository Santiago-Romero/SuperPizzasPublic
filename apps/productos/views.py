from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *


def gestionar_producto(request, id_producto=None):
    """
    Permite la creación y modificación de productos
    :param request:
    :param id_producto:
    :return:
    """
    if id_producto:
        producto = get_object_or_404(Producto, id=id_producto)
    else:
        producto = None
    form = ProductoForm(instance=producto)
    productos = Producto.objects.all()
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente')
            return redirect('productos:registrar')
        else:
            messages.error(request, 'Por favor verificar los campos en rojo')
    return render(request, 'productos/gestionar_producto.html', {'form': form, 'producto': producto, 'productos': productos})


def eliminar_producto(request, id_producto):
    """
    Permite la eliminación de productos
    :param request:
    :param id_producto:
    :return:
    """
    producto = get_object_or_404(Producto, id=id_producto)
    producto.delete()
    messages.success(request, 'Producto eliminado correctamente')

    return redirect('productos:registrar')