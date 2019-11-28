from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *


def gestionar_pizza(request, id_pizza=None):
    if request.user.is_anonymous:
        return render(request,"404.html",{})
    else:
        if((request.user.usuario.rol=='a' or request.user.usuario.rol=='d') and request.tenant.working==True):
            if id_pizza:
                pizza = get_object_or_404(Pizza, id=id_pizza)
            else:
                pizza = None
            form = PizzaForm(instance=pizza)
            pizzas = Pizza.objects.all()
            if request.method == 'POST':
                form = PizzaForm(request.POST, instance=pizza)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Pizza creado correctamente')
                    return redirect('pizzas:registrar')
                else:
                    messages.error(request, 'Por favor verificar los campos en rojo')
            return render(request, 'pizzas/gestionar_pizza.html', {'form': form, 'pizza': pizza, 'pizzas': pizzas})
        else:
            return render(request,"404.html",{})


def eliminar_pizza(request, id_pizza):
    if request.user.is_anonymous:
        return render(request,"404.html",{})
    else:
        if((request.user.usuario.rol=='a' or request.user.usuario.rol=='d') and request.tenant.working==True):
            pizza = get_object_or_404(Pizza, id=id_pizza)
            pizza.delete()
            messages.success(request, 'Pizza eliminado correctamente')

            return redirect('pizzas:registrar')
        else:
            return render(request,"404.html",{})