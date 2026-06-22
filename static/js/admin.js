
// Variable global para el conteo de alertas visuales en el Navbar
let totalNotificaciones = 0;

/**
 * 1. NAVEGACIÓN ENTRE SECCIONES (SIDEBAR)
 * Alterna la visibilidad de los contenedores del dashboard sin recargar la página.
 */
function cambiarSeccionLocal(idSeccion) {
    // Ocultar todas las secciones con la clase común
    document.querySelectorAll(".seccion-admin").forEach(sec => {
        sec.style.display = "none";
    });

    // Ocultar de igual forma el iframe externo si estuviera activo
    const iframe = document.getElementById('marco-externo');
    if (iframe) iframe.style.display = 'none';

    // Mostrar la sección solicitada
    const seccionObjetivo = document.getElementById(idSeccion);
    if (seccionObjetivo) {
        seccionObjetivo.style.display = "block";
    }
}

/**
 * 2. COMPATIBILIDAD CON IFRAME
 * Mantiene la carga de archivos o vistas externas si se requiere
 */
function cargarHTML(url) {
    document.querySelectorAll('.seccion-admin').forEach(sec => {
        sec.style.display = 'none';
    });

    const iframe = document.getElementById('marco-externo');
    if (iframe) {
        iframe.src = url;
        iframe.style.display = 'block';
    }
}

/**
 * 3. SISTEMA VISUAL DE NOTIFICACIONES DENTRO DEL PANEL
 * Agrega dinámicamente burbujas de notificación en el Navbar superior.
 */
function agregarNotificacionVisual(mensaje, icono, color) {
    totalNotificaciones++;

    const badge = document.getElementById("badge-notificaciones");
    if (badge) {
        badge.innerText = totalNotificaciones;
        badge.style.display = "block";
    }

    const menu = document.getElementById("menu-notificaciones");
    if (menu) {
        const item = document.createElement("li");
        item.innerHTML = `
            <a class="dropdown-item py-2" href="#" style="border-bottom: 1px solid rgba(165,201,202,0.25); color: inherit;">
                <i class="fas ${icono} text-${color} me-2"></i>
                ${mensaje}
                <br>
                <small class="text-muted ms-4" style="font-size: 0.7rem;">
                    Justo ahora
                </small>
            </a>
        `;
        // Insertar al inicio de la lista, justo debajo del encabezado
        menu.insertBefore(item, menu.children[1]);
    }
}

/**
 * 4. CONFIGURACIÓN PERSONALIZADA DE SWEETALERT2
 * Adapta los cuadros de diálogo a la paleta de colores de tu CSS (#EEF8F5, #395B64)
 */
const darkModeSwal = Swal.mixin({
    background: "#EEF8F5",
    color: "#2C3333",
    confirmButtonColor: "#395B64",
    cancelButtonColor: "#4a6370",
    customClass: {
        popup: 'swal-hebratech'
    }
});

/**
 * 5. CONTROL DE VISTAS DE CONTRASEÑAS (OJO MÁGICO)
 */
function togglePasswordVisibility() {
    const input = document.getElementById('input-password');
    const icono = document.getElementById('icon-ojo');
    if (input && icono) {
        if (input.type === 'password') {
            input.type = 'text';
            icono.classList.replace('fa-eye', 'fa-eye-slash');
        } else {
            input.type = 'password',
            icono.classList.replace('fa-eye-slash', 'fa-eye');
        }
    }
}

/**
 * 6. ACCIONES RÁPIDAS PARA ALERTAS E INCIDENCIAS DEL DASHBOARD
 */
function resolverIncidencia() {
    darkModeSwal.fire({
        icon: 'info',
        title: 'Atendiendo Incidencia',
        text: 'Se ha enviado una alerta al supervisor de la Línea 3 (Corte).',
    });
}

function formularioOperario() {
    darkModeSwal.fire({
        title: 'Asignar Nueva Tarea',
        text: 'Abre el módulo de operarios en el menú lateral para asignaciones directas en la base de datos.',
        icon: 'warning'
    });
}

function formularioCliente() {
    darkModeSwal.fire({
        title: 'Crear Nueva Orden',
        text: 'Redireccionando al módulo de órdenes comerciales...',
        icon: 'info'
    });
}

function formularioProveedor() {
    darkModeSwal.fire({
        title: 'Solicitar Insumos',
        text: 'Abriendo orden de compra automática para Stock Crítico de materia prima.',
        icon: 'info'
    });
}

/**
 * 7. INICIALIZACIÓN DE COMPONENTES AL CARGAR EL DOM
 * Renderiza la gráfica de Chart.js y maneja el temporizador del mensaje de bienvenida.
 */
document.addEventListener("DOMContentLoaded", () => {
    
    // Configuración de la gráfica de líneas de producción
    const canvasGrafica = document.getElementById('graficaProduccion');
    if (canvasGrafica) {
        const ctx = canvasGrafica.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'],
                datasets: [{
                    label: 'Eficiencia de Producción (%)',
                    data: [75, 82, 60, 88, 92, 79],
                    borderColor: '#395B64',
                    backgroundColor: 'rgba(57, 91, 100, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true, labels: { color: '#2C3333' } }
                },
                scales: {
                    y: { grid: { color: 'rgba(0,0,0,0.05)' }, ticks: { color: '#2C3333' } },
                    x: { grid: { display: false }, ticks: { color: '#2C3333' } }
                }
            }
        });
    }

    // Efecto suave de desvanecimiento para el saludo de bienvenida (se oculta a los 5 segundos)
    const msjBienvenida = document.getElementById('mensaje-bienvenida');
    if (msjBienvenida) {
        setTimeout(() => {
            msjBienvenida.style.transition = 'opacity 0.5s ease';
            msjBienvenida.style.opacity = '0';
            setTimeout(() => {
                msjBienvenida.style.display = 'none';
            }, 500);
        }, 5000);
    }
});