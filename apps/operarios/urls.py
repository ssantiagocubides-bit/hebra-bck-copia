from django.urls import path
from . import views

app_name = 'operarios'

urlpatterns = [

    # ------------------------------------------------------------------
    # Tablero principal — renderiza el HTML del Kanban
    # GET /operario/
    # ------------------------------------------------------------------
    path(
        '',
        views.tablero_operario,
        name='tablero'
    ),

    # ------------------------------------------------------------------
    # API — Tareas asignadas al operario logueado
    # GET /operario/api/tareas/
    # ------------------------------------------------------------------
    path(
        'api/tareas/',
        views.api_tareas,
        name='api_tareas'
    ),

    # ------------------------------------------------------------------
    # API — Guardar nuevo reporte (incidencia)
    # POST /operario/api/reporte/
    # ------------------------------------------------------------------
    path(
        'api/reporte/',
        views.api_guardar_reporte,
        name='api_guardar_reporte'
    ),

    # ------------------------------------------------------------------
    # API — Historial de reportes del operario
    # GET /operario/api/reportes/
    # ------------------------------------------------------------------
    path(
        'api/reportes/',
        views.api_historial_reportes,
        name='api_historial_reportes'
    ),

    # ------------------------------------------------------------------
    # API — Actualizar estado de una asignación (drag & drop Kanban)
    # POST /operario/api/tarea/<id>/estado/
    # ------------------------------------------------------------------
    path(
        'api/tarea/<int:id_asignacion>/estado/',
        views.api_actualizar_estado,
        name='api_actualizar_estado'
    ),

]