
from django.urls import path, include
from apps.franquicias.views import home, inicio_tenants, configuraciones,informacion, factura_PDF,renuncia, ordenar,\
 CartAgregar,CartListar, CartDelete,AgregarCantidadCarrito,CartComprar,CartSuccess
from apps.usuarios.views import inicio_sesion, cerrar_sesion,gestionar_cliente, check_email
from django.conf.urls import url

urlpatterns = [
    path('', inicio_tenants, name='inicio_t'),
    path('admin/', home, name='home'),
    path('login/', inicio_sesion,name='login'), 
    path('accounts/', include('allauth.urls')),
    path('cerrar_sesion/',cerrar_sesion, name='cerrar_sesion'),
    path('admin/pizzas/', include('apps.pizzas.urls', namespace='pizzas')),
    path('admin/usuarios/', include('apps.usuarios.urls', namespace='usuarios')),
    path('registroclientes/',gestionar_cliente,name='registro'),  
    path('validate_email/', check_email, name='check_email'),  
    path('admin/ingredientes/', include('apps.ingredientes.urls', namespace='ingredientes')),
    path('admin/configuraciones/',configuraciones, name='configuraciones'),
    path('admin/info/',informacion,name='info'),
    path('ordenar/',ordenar,name='ordenar'),
    #carrito de compras
    path('add/', CartAgregar.as_view(), name='cart_agregar'),
    path('lista_compra', CartListar.as_view(), name='cart_listar'),
    path('borrar_carrito', CartDelete.as_view(), name='cart_eliminar'),
    path('agregar_cantidades', AgregarCantidadCarrito.as_view(), name='cart_cantidades'),
    path('comprar', CartComprar.as_view(), name='cart_comprar'),
    path('compra_exitosa', CartSuccess.as_view(), name='cart_success'),
    url('reporte/(?P<id_factura>[0-9]+)$',factura_PDF, name="reporte_personas_pdf"),


]