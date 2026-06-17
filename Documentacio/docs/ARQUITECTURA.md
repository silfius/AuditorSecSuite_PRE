# ARQUITECTURA — AuditorSecSuite_PRE

Stack Docker-first con Django y PostgreSQL. Modelos iniciales: Activo, Auditoria, AuditoriaActivo, Finding. Motores futuros aislados: testssl/SSLyze, Nuclei, ZAP, Greenbone.

## Inventario de activos

El inventario utiliza `Activo`, `ActivoForm`, `asset_list`, `asset_create` y `asset_update`. La autorización del activo se mantiene como guardarraíl funcional antes de cualquier futura ejecución de motores.

## Base visual mínima

La interfaz mantiene CSS propio en `core/base.html` como base inicial: página con cabecera, toolbar, botones, tarjetas, tablas, formularios en grid, avisos y chips semánticos. Es una solución ligera previa a decidir si conviene extraer CSS estático o adoptar un sistema de diseño externo.

## Auditorías con activos autorizados

`AuditoriaForm` filtra activos auditables y valida server-side que solo se vinculen activos con `Activo.puede_auditarse()`. La relación se persiste mediante `AuditoriaActivo`.

## Findings manuales

`FindingForm` valida server-side que el activo seleccionado esté vinculado a la auditoría mediante `AuditoriaActivo`. No ejecuta motores ni genera findings automáticos.

## Selector dinámico auditoría-activo en Findings

El formulario de Findings usa un endpoint autenticado para cargar dinámicamente los activos auditables de la auditoría seleccionada. La validación server-side de `FindingForm` sigue siendo la autoridad funcional.\n\n## Detalles de auditorías y findings

Las vistas de detalle son de lectura operativa y mantienen `login_required`. `audit_detail` muestra datos de auditoría, activos vinculados y findings asociados. `finding_detail` muestra contexto de auditoría, activo y campos descriptivos del hallazgo. Ninguna vista ejecuta motores técnicos.\n

### Cierre detalle operativo `v0.2.6-pre`

Las vistas `audit_detail` y `finding_detail` consolidan una capa de trazabilidad de lectura. Se mantiene separación estricta entre visualización operativa y ejecución técnica: ninguna vista de detalle ejecuta motores ni automatismos.

## Checks seguros planificados

`CheckDefinition` define checks técnicos de forma declarativa. `AuditCheckPlan` permite planificar checks sobre una auditoría y un activo vinculado/autorizado.

Esta capa no ejecuta motores, no contiene comandos y no realiza llamadas de red. Su función es preparar el control operativo previo a futuras integraciones técnicas.

### Catálogo inicial de checks seguros

`CheckDefinition` recibe una semilla inicial mediante migración de datos. El catálogo es declarativo y no añade capa de ejecución. La futura integración de motores deberá partir de estos identificadores sin convertir la planificación en ejecución automática.

### Aplicabilidad de checks por tipo de activo

`CheckDefinition` incorpora normalización de alias entre tipos técnicos de check (`web`, `domain`, `ip`, `host`) y tipos reales de `Activo` (`url`, `dominio`, `host`, `servicio`, `contenedor`). `AuditCheckPlan.clean()` valida la coherencia en backend antes de guardar.

<!-- AUDITORSECSUITE_CHECK_APPLICABILITY_8B_VALIDATION_20260617 -->
### Evidencia de validación — Bloque 8B aplicabilidad de checks por tipo de activo

Fecha: 2026-06-17.

Resultado validado:

- Versión de trabajo: `0.2.9-pre`.
- `CheckDefinition` incorpora normalización de alias entre tipos del catálogo (`web`, `domain`, `ip`, `host`) y tipos reales de activo (`url`, `dominio`, `host`, `servicio`, `contenedor`).
- `CheckDefinition.applies_to_asset()` valida aplicabilidad sin ejecutar red ni motores.
- `AuditCheckPlan.clean()` bloquea en backend checks no aplicables al tipo de activo.
- `AuditCheckPlanForm` filtra checks activos, no intrusivos y aplicables al activo seleccionado.
- POST manipulado con check DNS sobre activo URL: bloqueado, sin crear plan.
- POST válido con check HTTP sobre activo URL: permitido.

Validaciones ejecutadas:

- `python manage.py check`: OK.
- `python manage.py makemigrations --check --dry-run`: OK.
- `SafeCheckApplicabilityTests`: 5 tests OK.
- `SafeCheckCatalogSeedTests` + `SafeCheckPlanningTests`: 8 tests OK.
- Suite `core`: 48 tests OK.
- Smoke funcional de aplicabilidad:
  - `HTTP_APPLIES_URL=True`.
  - `DNS_APPLIES_URL=False`.
  - `INVALID_POST_STATUS=200`.
  - `INVALID_POST_CREATED=False`.
  - `VALID_POST_STATUS=302`.
  - `NO_AUTOMATIC_FINDINGS_CREATED=1`.
  - `NO_ENGINE_EXECUTION_TRIGGERED=1`.
  - `OK_APPLICABILITY_FUNCTIONAL_SMOKE=1`.
- Auditoría anti-ejecución: sin `subprocess`, `os.system`, `Popen`, `requests.` ni `socket.` en código del bloque.
- Security audit: `OK_SECURITY_AUDIT=1`.
- Validadores documentales/proyecto: `OK_DOCUMENTATION_ALIGNMENT=1` y `OK_PROJECT_ALIGNMENT=1`.
- `git diff --check`: OK.

Conclusión: la planificación de checks ya queda protegida contra combinaciones incoherentes por tipo de activo, sin introducir ejecución técnica.
