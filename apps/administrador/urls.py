from django.urls import path
from . import views

urlpatterns = [
    # Ruta principal del panel
    path('', views.panel_admin, name='panel_admin'),
    
    # Endpoints de Usuarios
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    
    # Endpoints de Tareas / Operarios
    path('tareas/crear/', views.crear_tarea, name='crear_tarea'),
    path('tareas/eliminar/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),
    
    # Endpoints de Órdenes / Clientes
    path('ordenes/crear/', views.crear_orden, name='crear_orden'),
    path('ordenes/eliminar/<int:orden_id>/', views.eliminar_orden, name='eliminar_orden'),
]


