from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Tarea, Orden
from .forms import UsuarioForm, TareaForm, OrdenForm

def panel_admin(request):
    """
    Vista principal que renderiza el tablero con todos los datos 
    y formularios necesarios en una sola carga.
    """
    contexto = {
        'usuarios': Usuario.objects.all(),
        'tareas': Tarea.objects.all(),
        'ordenes': Orden.objects.all(),
        'form_usuario': UsuarioForm(),
        'form_tarea': TareaForm(),
        'form_orden': OrdenForm(),
    }
    return render(request, 'admin.html', contexto)

# --- OPERACIONES DEL MÓDULO DE USUARIOS ---
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('administrador:panel_admin')  # 🛠️ Corregido: Se agregó el namespace

def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    return redirect('administrador:panel_admin')  # 🛠️ Corregido: Se agregó el namespace

# --- OPERACIONES DEL MÓDULO DE TAREAS (OPERARIOS) ---
def crear_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('administrador:panel_admin')  # 🛠️ Corregido: Se agregó el namespace

def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    tarea.delete()
    return redirect('administrador:panel_admin')  # 🛠️ Corregido: Se agregó el namespace

# --- OPERACIONES DEL MÓDULO DE ÓRDENES (CLIENTES) ---
def crear_orden(request):
    if request.method == 'POST':
        form = OrdenForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('administrador:panel_admin')  # 🛠️ Corregido: Se agregó el namespace

def eliminar_orden(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)
    orden.delete()
    return redirect('administrador:panel_admin')  # 🛠️ Corregido: Se agregó el namespace