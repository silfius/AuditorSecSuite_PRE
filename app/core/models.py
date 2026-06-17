from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

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



class CheckDefinition(models.Model):
    """Definición declarativa de checks técnicos seguros.

    No contiene comandos, argumentos ejecutables ni lógica de ejecución.
    """

    CATEGORY_TLS = "tls"
    CATEGORY_HTTP = "http"
    CATEGORY_DNS = "dns"
    CATEGORY_INFRA = "infra"
    CATEGORY_WEB = "web"
    CATEGORY_INTERNAL = "internal"

    CATEGORY_CHOICES = [
        (CATEGORY_TLS, "TLS / Certificados"),
        (CATEGORY_HTTP, "HTTP / Cabeceras"),
        (CATEGORY_DNS, "DNS"),
        (CATEGORY_INFRA, "Infraestructura"),
        (CATEGORY_WEB, "Aplicación web"),
        (CATEGORY_INTERNAL, "Control interno"),
    ]

    ENGINE_MANUAL = "manual"
    ENGINE_NOOP = "noop"
    ENGINE_FUTURE_TESTSSL = "future_testssl"
    ENGINE_FUTURE_SSLYZE = "future_sslyze"
    ENGINE_FUTURE_ZAP = "future_zap"
    ENGINE_FUTURE_GREENBONE = "future_greenbone"

    ENGINE_CHOICES = [
        (ENGINE_MANUAL, "Manual / revisable"),
        (ENGINE_NOOP, "Simulado / noop"),
        (ENGINE_FUTURE_TESTSSL, "Futuro testssl"),
        (ENGINE_FUTURE_SSLYZE, "Futuro SSLyze"),
        (ENGINE_FUTURE_ZAP, "Futuro ZAP"),
        (ENGINE_FUTURE_GREENBONE, "Futuro Greenbone"),
    ]

    RISK_PASSIVE = "passive"
    RISK_CONTROLLED = "controlled"
    RISK_INTRUSIVE = "intrusive"

    RISK_CHOICES = [
        (RISK_PASSIVE, "Pasivo / seguro"),
        (RISK_CONTROLLED, "Controlado"),
        (RISK_INTRUSIVE, "Intrusivo — no permitido todavía"),
    ]

    codigo = models.SlugField(max_length=80, unique=True)
    nombre = models.CharField(max_length=160)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=32, choices=CATEGORY_CHOICES, default=CATEGORY_INTERNAL)
    engine_key = models.CharField(max_length=40, choices=ENGINE_CHOICES, default=ENGINE_MANUAL)
    tipo_activo_aplicable = models.CharField(max_length=80, blank=True)
    is_enabled = models.BooleanField(default=True)
    nivel_riesgo_operativo = models.CharField(
        max_length=32,
        choices=RISK_CHOICES,
        default=RISK_PASSIVE,
    )
    requiere_autorizacion = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["categoria", "codigo"]

    def __str__(self):
        return f"{self.codigo} — {self.nombre}"


    ASSET_TYPE_ALIASES = {
        "url": {"url", "web"},
        "web": {"url", "web"},
        "dominio": {"dominio", "domain", "dns"},
        "domain": {"dominio", "domain", "dns"},
        "host": {"host", "ip"},
        "ip": {"host", "ip"},
        "servicio": {"servicio", "service"},
        "service": {"servicio", "service"},
        "contenedor": {"contenedor", "container"},
        "container": {"contenedor", "container"},
    }

    def applicable_asset_tokens(self):
        if not self.tipo_activo_aplicable:
            return set()
        return {
            token.strip().lower()
            for token in self.tipo_activo_aplicable.split(",")
            if token.strip()
        }

    @classmethod
    def normalized_asset_type_tokens(cls, asset_or_type):
        if asset_or_type is None:
            return set()

        raw_type = getattr(asset_or_type, "tipo", asset_or_type)
        if raw_type is None:
            return set()

        token = str(raw_type).strip().lower()
        if not token:
            return set()

        return cls.ASSET_TYPE_ALIASES.get(token, {token})

    def applies_to_asset(self, asset):
        allowed_tokens = self.applicable_asset_tokens()
        if not allowed_tokens:
            return True

        asset_tokens = self.normalized_asset_type_tokens(asset)
        return bool(allowed_tokens.intersection(asset_tokens))

    def get_applicable_asset_tokens_display(self):
        tokens = sorted(self.applicable_asset_tokens())
        return ", ".join(tokens) if tokens else "Todos"


class AuditCheckPlan(models.Model):
    """Planificación segura de checks sobre una auditoría y activo autorizado.

    Esta entidad no ejecuta motores. Solo registra intención/planificación.
    """

    STATE_PLANNED = "planned"
    STATE_READY = "ready"
    STATE_BLOCKED = "blocked"
    STATE_OMITTED = "omitted"

    STATE_CHOICES = [
        (STATE_PLANNED, "Planificado"),
        (STATE_READY, "Preparado sin ejecutar"),
        (STATE_BLOCKED, "Bloqueado"),
        (STATE_OMITTED, "Omitido"),
    ]

    auditoria = models.ForeignKey(Auditoria, on_delete=models.CASCADE, related_name="check_plans")
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE, related_name="check_plans")
    check_definition = models.ForeignKey(CheckDefinition, on_delete=models.PROTECT, related_name="audit_plans")
    estado = models.CharField(max_length=24, choices=STATE_CHOICES, default=STATE_PLANNED)
    motivo_bloqueo = models.TextField(blank=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_check_plans",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["auditoria", "activo", "check_definition"]
        constraints = [
            models.UniqueConstraint(
                fields=["auditoria", "activo", "check_definition"],
                name="unique_audit_asset_check_plan",
            )
        ]

    def __str__(self):
        return f"{self.auditoria} · {self.activo} · {self.check_definition}"

    def clean(self):
        super().clean()

        if self.activo_id and not self.activo.puede_auditarse():
            raise ValidationError({
                "activo": "Solo se pueden planificar checks sobre activos activos y autorizados."
            })

        if self.auditoria_id and self.activo_id:
            vinculado = AuditoriaActivo.objects.filter(
                auditoria=self.auditoria,
                activo=self.activo,
            ).exists()
            if not vinculado:
                raise ValidationError({
                    "activo": "El activo debe estar vinculado a la auditoría seleccionada."
                })

        if self.check_definition_id:
            if not self.check_definition.is_enabled:
                raise ValidationError({
                    "check_definition": "No se puede planificar un check desactivado."
                })
            if self.check_definition.nivel_riesgo_operativo == CheckDefinition.RISK_INTRUSIVE:
                raise ValidationError({
                    "check_definition": "Los checks intrusivos no están permitidos en esta fase."
                })

            if self.activo_id and not self.check_definition.applies_to_asset(self.activo):
                raise ValidationError({
                    "check_definition": "El check seleccionado no aplica al tipo de activo informado."
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
