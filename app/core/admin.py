from django.contrib import admin
from .models import Activo, Auditoria, AuditoriaActivo, Finding

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
