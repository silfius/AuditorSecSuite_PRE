from django.conf import settings
from django.db import models

class Activo(models.Model):
    class Tipo(models.TextChoices):
        HOST = "host", "Host/IP"
        URL = "url", "URL"
        DOMINIO = "dominio", "Dominio"
        SERVICIO = "servicio", "Servicio"
        CONTENEDOR = "contenedor", "Contenedor"

    nombre = models.CharField(max_length=180)
    tipo = models.CharField(max_length=30, choices=Tipo.choices)
    valor = models.CharField(max_length=255)
    entorno = models.CharField(max_length=80, blank=True)
    autorizado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    notas = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre"]
        constraints = [
            models.UniqueConstraint(fields=["tipo", "valor"], name="uniq_activo_tipo_valor")
        ]

    def __str__(self):
        return f"{self.nombre} ({self.valor})"

    def puede_auditarse(self):
        return self.activo and self.autorizado


class Auditoria(models.Model):
    class Estado(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        PLANIFICADA = "planificada", "Planificada"
        EN_CURSO = "en_curso", "En curso"
        FINALIZADA = "finalizada", "Finalizada"
        CANCELADA = "cancelada", "Cancelada"

    class Perfil(models.TextChoices):
        INVENTARIO = "inventario", "Inventario seguro"
        WEB_BASICO = "web_basico", "Web básico"
        TLS = "tls", "TLS/certificados"
        NUCLEI_SEGURO = "nuclei_seguro", "Nuclei seguro"
        GREENBONE = "greenbone", "Greenbone infraestructura"

    nombre = models.CharField(max_length=180)
    alcance = models.TextField()
    perfil = models.CharField(max_length=40, choices=Perfil.choices, default=Perfil.INVENTARIO)
    estado = models.CharField(max_length=40, choices=Estado.choices, default=Estado.BORRADOR)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado_en"]

    def __str__(self):
        return self.nombre


class AuditoriaActivo(models.Model):
    auditoria = models.ForeignKey(Auditoria, on_delete=models.CASCADE, related_name="auditoria_activos")
    activo = models.ForeignKey(Activo, on_delete=models.PROTECT, related_name="auditoria_activos")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["auditoria", "activo"], name="uniq_auditoria_activo")
        ]


class Finding(models.Model):
    class Severidad(models.TextChoices):
        INFO = "info", "Informativa"
        BAJA = "baja", "Baja"
        MEDIA = "media", "Media"
        ALTA = "alta", "Alta"
        CRITICA = "critica", "Crítica"

    class Estado(models.TextChoices):
        NUEVO = "nuevo", "Nuevo"
        REVISADO = "revisado", "Revisado"
        FALSO_POSITIVO = "falso_positivo", "Falso positivo"
        ACEPTADO = "aceptado", "Riesgo aceptado"
        CORREGIDO = "corregido", "Corregido"

    auditoria = models.ForeignKey(Auditoria, on_delete=models.CASCADE, related_name="findings")
    activo = models.ForeignKey(Activo, on_delete=models.PROTECT, related_name="findings")
    titulo = models.CharField(max_length=220)
    severidad = models.CharField(max_length=20, choices=Severidad.choices, default=Severidad.INFO)
    estado = models.CharField(max_length=30, choices=Estado.choices, default=Estado.NUEVO)
    herramienta = models.CharField(max_length=80, blank=True)
    descripcion = models.TextField()
    evidencia = models.TextField(blank=True)
    recomendacion = models.TextField(blank=True)
    referencia = models.CharField(max_length=255, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["auditoria", "activo", "titulo"]

    def __str__(self):
        return f"[{self.get_severidad_display()}] {self.titulo}"
