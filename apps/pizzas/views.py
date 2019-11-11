from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from datetime import date

def gestionar_pizza(request, id_pizza=None):
    """
    Permite la creación y modificación de pizzas
    :param request:
    :param id_pizza:
    :return:
    """
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


def eliminar_pizza(request, id_pizza):
    """
    Permite la eliminación de pizzas
    :param request:
    :param id_pizza:
    :return:
    """
    pizza = get_object_or_404(Pizza, id=id_pizza)
    pizza.delete()
    messages.success(request, 'Pizza eliminado correctamente')

    return redirect('pizzas:registrar')

def informacion(request):
    inicio=request.tenant.fecha_corte
    dias=inicio-date.today()
    context={'dias':dias.days}
    return render(request,'info.html',context)