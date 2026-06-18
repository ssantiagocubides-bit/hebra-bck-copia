# apps/clientes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Sin espacios raros, solo la palabra limpia
    path('portal/', views.cliente_portal, name='cliente_portal'),
    path('orden-exitosa/<int:idOrden>/', views.orden_exitosa, name='orden_exitosa'),
]