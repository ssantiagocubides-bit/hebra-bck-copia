from django.db import models

class Usuario(models.Model):
    """
    Modelo para la gestión de usuarios del sistema y control de roles.
    """
    ROLES_CHOICES = [
        ('administrador', 'Administrador'),
        ('operario', 'Operario'),
        ('cliente', 'Cliente'),
        ('proveedor', 'Proveedor'),
    ]
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    rol = models.CharField(max_length=50, choices=ROLES_CHOICES)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.get_rol_display()})"


class Tarea(models.Model):
    """
    Modelo para la asignación y monitoreo de tareas operativas en las líneas de producción.
    """
    PRIORIDADES_CHOICES = [
        ('Baja', 'Baja'), 
        ('Media', 'Media'), 
        ('Alta', 'Alta'), 
        ('Urgente', 'Urgente')
    ]
    
    ESTADOS_CHOICES = [
        ('Pendiente', 'Pendiente'), 
        ('En proceso', 'En proceso'), 
        ('Completada', 'Completada')
    ]
    
    operario = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    linea = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_limite = models.DateField()
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES_CHOICES, default='Media')
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='Pendiente')
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        # CORREGIDO: Se cambió self.tarea por self.descripcion
        return f"{self.descripcion} - {self.operario} ({self.estado})"


class Orden(models.Model):
    """
    Modelo para el seguimiento de órdenes comerciales, solicitudes de clientes y estado de pagos.
    """
    PAGOS_CHOICES = [
        ('Pendiente', 'Pendiente'), 
        ('Anticipo pagado', 'Anticipo pagado'), 
        ('Pagado completo', 'Pagado completo')
    ]
    
    ESTADOS_ORDEN_CHOICES = [
        ('En proceso', 'En proceso'), 
        ('Completada', 'Completada'), 
        ('Cancelada', 'Cancelada')
    ]

    cliente = models.CharField(max_length=100)
    nit = models.CharField(max_length=50, blank=True, null=True, verbose_name="NIT / Documento")
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    producto = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    fecha_entrega = models.DateField()
    estado_pago = models.CharField(max_length=50, choices=PAGOS_CHOICES, default='Pendiente')
    estado_orden = models.CharField(max_length=50, choices=ESTADOS_ORDEN_CHOICES, default='En proceso')
    especificaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.cliente} ({self.producto})"