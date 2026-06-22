import json
import logging
from datetime import date

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  # solo activo si settings.DEBUG=True

from .models import Operario, AsignacionTarea, Incidencia

logger = logging.getLogger(__name__)

ESTADOS_VALIDOS_ASIGNACION = ['Pendiente', 'En Progreso', 'Completada', 'Cancelada']

# tipoIncidencia es varchar(50) libre en la BD (no enum/choices), así que solo
# validamos longitud máxima, no una lista cerrada de valores.
TIPO_INCIDENCIA_MAX_LEN = 50


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_operario_actual(request):
    """
    Obtiene el Operario logueado desde la sesión.
    La sesión debe tener 'idOperario' guardado al hacer login.
    Retorna el objeto Operario o None si no hay sesión activa o no está activo.
    """
    id_operario = request.session.get('idOperario')
    if not id_operario:
        return None
    try:
        return Operario.objects.select_related('idUsuario').get(
            idOperario=id_operario,
            estado='activo'
        )
    except Operario.DoesNotExist:
        return None


def _get_operario_o_dev(request):
    """
    Punto único para el fallback de desarrollo.
    SOLO usa el operario id=1 si DEBUG está activo. En producción
    (DEBUG=False) nunca inventa un operario: si no hay sesión, devuelve None.

    Esto evita que el fallback de "pruebas" quede activo por accidente
    cuando se despliegue el proyecto.
    """
    operario = _get_operario_actual(request)
    if operario is None and settings.DEBUG:
        try:
            operario = Operario.objects.select_related('idUsuario').get(idOperario=1)
            logger.warning("Usando operario id=1 de fallback (DEBUG=True). No usar en producción.")
        except Operario.DoesNotExist:
            operario = None
    return operario


# ---------------------------------------------------------------------------
# Vista principal — Tablero Kanban
# ---------------------------------------------------------------------------

def tablero_operario(request):
    """
    GET /operario/
    Renderiza el tablero Kanban con las tareas asignadas al operario logueado.
    """
    operario = _get_operario_o_dev(request)

    asignaciones = []
    if operario:
        asignaciones = (
            AsignacionTarea.objects
            .filter(idOperario=operario)
            .select_related('idTarea')
            .order_by('fechaInicio')
        )

    contadores = {
        'pendiente':   sum(1 for a in asignaciones if a.estado == 'Pendiente'),
        'en_progreso': sum(1 for a in asignaciones if a.estado == 'En Progreso'),
        'completada':  sum(1 for a in asignaciones if a.estado == 'Completada'),
    }

    context = {
        'operario':     operario,
        'asignaciones': asignaciones,
        'contadores':   contadores,
    }
    return render(request, 'operario/tablero.html', context)


# ---------------------------------------------------------------------------
# API — Tareas del operario (JSON para el JS del Kanban)
# ---------------------------------------------------------------------------

def api_tareas(request):
    """
    GET /operario/api/tareas/
    """
    operario = _get_operario_o_dev(request)

    if operario is None:
        return JsonResponse({'tareas': [], 'error': 'Sesión no válida'}, status=401)

    asignaciones = (
        AsignacionTarea.objects
        .filter(idOperario=operario)
        .select_related('idTarea')
        .order_by('fechaInicio')
    )

    tareas = [
        {
            'idAsignacion':      a.idAsignacion,
            'idTarea':           a.idTarea.idTarea,
            'nombreTarea':       a.idTarea.nombreTarea,
            'descripcionTarea':  a.idTarea.descripcionTarea,
            'proceso':           a.idTarea.proceso,
            'complejidad':       a.idTarea.complejidad,
            'descripcion':       a.descripcion,
            'fechaInicio':       str(a.fechaInicio),
            'fechaFinalizacion': str(a.fechaFinalizacion) if a.fechaFinalizacion else None,
            'estado':            a.estado,
            'prioridad':         a.prioridad,
            'horasEstimadas':    float(a.horasEstimadas),
            'horasReales':       float(a.horasReales) if a.horasReales else None,
        }
        for a in asignaciones
    ]

    return JsonResponse({'tareas': tareas})


# ---------------------------------------------------------------------------
# API — Registrar incidencia
# ---------------------------------------------------------------------------

@require_POST
@csrf_exempt  # TODO: quitar esta línea cuando el login/sesión esté integrado y probado con CSRF real
def api_guardar_reporte(request):
    """
    POST /operario/api/reporte/

    Body JSON esperado:
    {
        "tipoIncidencia":  "Error de corte",
        "descripcion":     "Texto del reporte...",
        "periodoEvaluado": "Junio 2026"   // opcional
    }
    """
    operario = _get_operario_o_dev(request)
    if operario is None:
        return JsonResponse({'ok': False, 'error': 'Sesión no válida'}, status=401)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'JSON inválido'}, status=400)

    if not isinstance(data, dict):
        return JsonResponse({'ok': False, 'error': 'Formato de datos inválido'}, status=400)

    # .strip() falla si el valor es None explícito en el JSON, por eso
    # se usa "or ''" antes de strip para blindar ambos casos (ausente o null)
    tipo        = (data.get('tipoIncidencia') or '').strip()
    descripcion = (data.get('descripcion') or '').strip()
    periodo     = (data.get('periodoEvaluado') or '').strip() or None

    errores = {}
    if not tipo:
        errores['tipoIncidencia'] = 'El tipo de incidencia es obligatorio'
    elif len(tipo) > TIPO_INCIDENCIA_MAX_LEN:
        errores['tipoIncidencia'] = f'El tipo de incidencia no puede superar los {TIPO_INCIDENCIA_MAX_LEN} caracteres'

    if not descripcion:
        errores['descripcion'] = 'La descripción es obligatoria'
    elif len(descripcion) < 10:
        errores['descripcion'] = 'La descripción debe tener al menos 10 caracteres'
    elif len(descripcion) > 2000:
        errores['descripcion'] = 'La descripción no puede superar los 2000 caracteres'

    if periodo and len(periodo) > 50:
        errores['periodoEvaluado'] = 'El periodo evaluado no puede superar los 50 caracteres'

    if errores:
        return JsonResponse({'ok': False, 'errores': errores}, status=400)

    try:
        incidencia = Incidencia.objects.create(
            idOperario      = operario,
            tipoIncidencia  = tipo,
            descripcion     = descripcion,
            periodoEvaluado = periodo,
            estado          = 'Generado',
            fechaGeneracion = date.today(),
        )
    except Exception:
        logger.exception("Error al crear incidencia para operario id=%s", operario.idOperario)
        return JsonResponse({'ok': False, 'error': 'No se pudo guardar el reporte. Intenta de nuevo.'}, status=500)

    return JsonResponse({
        'ok':           True,
        'idIncidencia': incidencia.idIncidencia,
        'mensaje':      'Reporte guardado correctamente',
        'fecha':        str(incidencia.fechaGeneracion),
    }, status=201)


# ---------------------------------------------------------------------------
# API — Historial de reportes del operario
# ---------------------------------------------------------------------------

def api_historial_reportes(request):
    """
    GET /operario/api/reportes/
    """
    operario = _get_operario_o_dev(request)
    if operario is None:
        return JsonResponse({'reportes': [], 'error': 'Sesión no válida'}, status=401)

    reportes_qs = (
        Incidencia.objects
        .filter(idOperario=operario)
        .order_by('-fechaGeneracion')[:20]
    )

    reportes = [
        {
            'idIncidencia':    r.idIncidencia,
            'tipoIncidencia':  r.tipoIncidencia,
            'descripcion':     (r.descripcion[:100] + '...') if len(r.descripcion) > 100 else r.descripcion,
            'periodoEvaluado': r.periodoEvaluado,
            'estado':          r.estado,
            'fechaGeneracion': str(r.fechaGeneracion),
            'fechaRevision':   str(r.fechaRevision) if r.fechaRevision else None,
        }
        for r in reportes_qs
    ]

    return JsonResponse({'reportes': reportes})


# ---------------------------------------------------------------------------
# API — Actualizar estado de una asignación (drag & drop Kanban)
# ---------------------------------------------------------------------------

@require_POST
@csrf_exempt  # TODO: quitar cuando el login esté integrado
def api_actualizar_estado(request, id_asignacion):
    """
    POST /operario/api/tarea/<id_asignacion>/estado/

    Body JSON esperado:
    {
        "estado": "En Progreso"   // Pendiente | En Progreso | Completada | Cancelada
    }
    """
    operario = _get_operario_o_dev(request)
    if operario is None:
        return JsonResponse({'ok': False, 'error': 'Sesión no válida'}, status=401)

    asignacion = get_object_or_404(
        AsignacionTarea, idAsignacion=id_asignacion, idOperario=operario
    )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'JSON inválido'}, status=400)

    nuevo_estado = (data.get('estado') or '').strip()
    if nuevo_estado not in ESTADOS_VALIDOS_ASIGNACION:
        return JsonResponse({
            'ok': False,
            'error': f'Estado inválido. Opciones: {ESTADOS_VALIDOS_ASIGNACION}'
        }, status=400)

    asignacion.estado = nuevo_estado
    if nuevo_estado == 'Completada' and not asignacion.fechaFinalizacion:
        asignacion.fechaFinalizacion = date.today()

    asignacion.save()

    return JsonResponse({
        'ok':     True,
        'estado': asignacion.estado,
        'fecha':  str(asignacion.fechaFinalizacion) if asignacion.fechaFinalizacion else None,
    })