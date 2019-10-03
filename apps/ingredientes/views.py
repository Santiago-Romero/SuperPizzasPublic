from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *


def gestionar_ingrediente(request, id_ingrediente=None):
    """
    Permite la creación y modificación de ingredientes
    :param request:
    :param id_ingrediente:
    :return:
    """
    if id_ingrediente:
        ingrediente = get_object_or_404(Ingrediente, id=id_ingrediente)
    else:
        ingrediente = None
    form = IngredienteForm(instance=ingrediente)
    ingredientes = Ingrediente.objects.all()
    if request.method == 'POST':
        form = IngredienteForm(request.POST, instance=ingrediente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingrediente creado correctamente')
            return redirect('ingredientes:registrar')
        else:
            messages.error(request, 'Por favor verificar los campos en rojo')
    return render(request, 'ingredientes/gestionar_ingrediente.html', {'form': form, 'ingrediente': ingrediente, 'ingredientes': ingredientes})


def eliminar_ingrediente(request, id_ingrediente):
    """
    Permite la eliminación de ingredientes
    :param request:
    :param id_ingrediente:
    :return:
    """
    ingrediente = get_object_or_404(Ingrediente, id=id_ingrediente)
    ingrediente.delete()
    messages.success(request, 'Ingrediente eliminado correctamente')

    return redirect('ingredientes:registrar')