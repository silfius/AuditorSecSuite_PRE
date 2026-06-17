from django.contrib import admin
from .models import Activo, Auditoria, AuditoriaActivo, Finding
from .models import CheckDefinition, AuditCheckPlan

@admin.register(Activo)
class ActivoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "valor", "entorno", "autorizado", "activo")
    list_filter = ("tipo", "entorno", "autorizado", "activo")
    search_fields = ("nombre", "valor", "notas")

class AuditoriaActivoInline(admin.TabularInline):
    model = AuditoriaActivo
    extra = 1

@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "perfil", "estado", "creado_en")
    list_filter = ("perfil", "estado")
    search_fields = ("nombre", "alcance")
    inlines = [AuditoriaActivoInline]

@admin.register(Finding)
class FindingAdmin(admin.ModelAdmin):
    list_display = ("titulo", "auditoria", "activo", "severidad", "estado", "herramienta")
    list_filter = ("severidad", "estado", "herramienta")
    search_fields = ("titulo", "descripcion", "evidencia", "recomendacion")



@admin.register(CheckDefinition)
class CheckDefinitionAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "categoria", "engine_key", "nivel_riesgo_operativo", "is_enabled")
    list_filter = ("categoria", "engine_key", "nivel_riesgo_operativo", "is_enabled")
    search_fields = ("codigo", "nombre", "descripcion")


@admin.register(AuditCheckPlan)
class AuditCheckPlanAdmin(admin.ModelAdmin):
    list_display = ("auditoria", "activo", "check_definition", "estado", "creado_por", "creado_en")
    list_filter = ("estado", "check_definition__categoria", "check_definition__nivel_riesgo_operativo")
    search_fields = ("check_definition__codigo", "check_definition__nombre")
