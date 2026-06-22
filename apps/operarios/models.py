from django.db import models


class Usuario(models.Model):
    """
    Tabla: usuarios
    Usuarios del sistema (administrador, operario, cliente).
    """
    ROL_CHOICES = [
        ('administrador', 'Administrador'),
        ('operario', 'Operario'),
        ('cliente', 'Cliente'),
    ]
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('reportado', 'Reportado'),
    ]

    idUsuario       = models.AutoField(primary_key=True)
    nombre          = models.CharField(max_length=100)
    apellido        = models.CharField(max_length=100)
    correoElectronico = models.CharField(max_length=200, unique=True)
    contrasena      = models.CharField(max_length=255)
    telefono        = models.CharField(max_length=20, null=True, blank=True)
    direccion       = models.CharField(max_length=255, null=True, blank=True)
    rol             = models.CharField(max_length=20, choices=ROL_CHOICES, default='cliente')
    estado          = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')

    class Meta:
        db_table = 'usuarios'
        managed = False  # Django NO toca esta tabla, ya existe en MySQL

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"


class Operario(models.Model):
    """
    Tabla: operarios
    Perfil extendido del operario. 1:1 con usuarios.
    """
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    idOperario   = models.AutoField(primary_key=True)
    idUsuario    = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        db_column='idUsuario',
        related_name='operario'
    )
    especialidad  = models.CharField(max_length=100)
    fechaIngreso  = models.DateField()
    estado        = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')

    class Meta:
        db_table = 'operarios'
        managed = False

    def __str__(self):
        return f"Operario #{self.idOperario} — {self.especialidad}"


class Tarea(models.Model):
    """
    Tabla: tareas
    Definición de cada tarea de producción.
    """
    COMPLEJIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]

    idTarea          = models.AutoField(primary_key=True)
    # idProduccion es FK a produccion — la dejamos como entero simple
    # para no tener que mapear toda la cadena ahora
    idProduccion     = models.IntegerField(null=True, blank=True)
    nombreTarea      = models.CharField(max_length=150)
    descripcionTarea = models.TextField()
    fechaCreacion    = models.DateField()
    proceso          = models.CharField(max_length=100)
    complejidad      = models.CharField(max_length=10, choices=COMPLEJIDAD_CHOICES)

    class Meta:
        db_table = 'tareas'
        managed = False

    def __str__(self):
        return self.nombreTarea


class AsignacionTarea(models.Model):
    """
    Tabla: asignacion_tareas
    Relaciona un operario con una tarea. Es lo que aparece en el Kanban.
    """
    ESTADO_CHOICES = [
        ('Pendiente',   'Pendiente'),
        ('En Progreso', 'En Progreso'),
        ('Completada',  'Completada'),
        ('Cancelada',   'Cancelada'),
    ]
    PRIORIDAD_CHOICES = [
        ('Baja',    'Baja'),
        ('Media',   'Media'),
        ('Alta',    'Alta'),
        ('Urgente', 'Urgente'),
    ]

    idAsignacion       = models.AutoField(primary_key=True)
    idTarea            = models.ForeignKey(
        Tarea,
        on_delete=models.CASCADE,
        db_column='idTarea',
        related_name='asignaciones'
    )
    idOperario         = models.ForeignKey(
        Operario,
        on_delete=models.CASCADE,
        db_column='idOperario',
        related_name='asignaciones'
    )
    descripcion        = models.TextField()
    fechaAsignacion    = models.DateField()
    fechaInicio        = models.DateField()
    fechaFinalizacion  = models.DateField(null=True, blank=True)
    estado             = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    prioridad          = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='Media')
    horasEstimadas     = models.DecimalField(max_digits=5, decimal_places=2)
    horasReales        = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'asignacion_tareas'
        managed = False

    def __str__(self):
        return f"Asignación #{self.idAsignacion} → {self.idTarea} [{self.estado}]"


class Incidencia(models.Model):
    """
    Tabla: incidencias
    Reportes generados por el operario sobre producción.
    Este es el modelo central del módulo.
    """
    ESTADO_CHOICES = [
        ('Generado',  'Generado'),
        ('Revisado',  'Revisado'),
        ('Pendiente', 'Pendiente'),
    ]

    idIncidencia     = models.AutoField(primary_key=True)
    idOperario       = models.ForeignKey(
        Operario,
        on_delete=models.CASCADE,
        db_column='idOperario',
        related_name='incidencias'
    )
    tipoIncidencia   = models.CharField(max_length=50)
    descripcion      = models.TextField()
    periodoEvaluado  = models.CharField(max_length=50, null=True, blank=True)
    estado           = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='Generado')
    fechaGeneracion  = models.DateField()
    fechaRevision    = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'incidencias'
        managed = False

    def __str__(self):
        return f"Reporte #{self.idIncidencia} — {self.tipoIncidencia} [{self.estado}]"
