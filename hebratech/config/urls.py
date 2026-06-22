from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.usuarios.urls')),
    path('clientes/', include('apps.clientes.urls')),
    path('produccion/', include('apps.produccion.urls')),
    
    # 🛠️ Corrección aquí: Pasamos una tupla (ruta, app_name) para que acepte el namespace
    path('operario/', include(('apps.operarios.urls', 'operarios'), namespace='operarios')),
    path('administrador/', include(('apps.administrador.urls', 'administrador'), namespace='administrador')),
]