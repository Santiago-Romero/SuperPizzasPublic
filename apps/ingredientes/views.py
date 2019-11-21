from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *


def gestionar_ingrediente(request, id_ingrediente=None):
    if((request.user.usuario.rol=='a' or request.user.usuario.rol=='d') and request.tenant.working==True):
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
    else:
        return render(request,"404.html",{})


def eliminar_ingrediente(request, id_ingrediente):
    if((request.user.usuario.rol=='a' or request.user.usuario.rol=='d') and request.tenant.working==True):
        ingrediente = get_object_or_404(Ingrediente, id=id_ingrediente)
        ingrediente.delete()
        messages.success(request, 'Ingrediente eliminado correctamente')

        return redirect('ingredientes:registrar')
    else:
        return render(request,"404.html",{})