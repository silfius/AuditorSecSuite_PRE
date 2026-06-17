# TESTING — AuditorSecSuite_PRE

Un cambio no está validado sin evidencia. Validaciones: compose config, Django check, makemigrations check, tests por riesgo, git diff check, security audit. Tests no ejecutarán escaneos reales.

## Inventario de activos autorizados

Cobertura prevista/ejecutada: `AssetFormTests`, `AssetViewsTests` y pruebas de modelo para asegurar que un activo solo es auditable si está activo y autorizado.

## Auditorías con activos autorizados

Cobertura prevista/ejecutada: `AuditFormTests` y `AuditViewsTests` para validar login requerido, creación, edición y rechazo de activos no auditables.

## Findings manuales

Cobertura prevista/ejecutada: `FindingFormTests` y `FindingViewsTests` para validar login requerido, creación, edición y rechazo de activos no vinculados a la auditoría.

## Selector dinámico Findings auditoría-activo

Cobertura: `FindingDynamicAssetSelectorTests` valida endpoint autenticado, exclusión de activos externos/no autorizados y presencia del hook JS en formulario.

### 2026-06-17 — Validación cierre selector dinámico Findings

Validaciones ejecutadas para cierre `v0.2.4-pre`:

- Build Docker.
- `python manage.py check`.
- `python manage.py makemigrations --check --dry-run`.
- Suite `core`: 30 tests OK.
- Security audit.
- Validadores de documentación y proyecto.
- `git diff --check`.
- Smoke HTTP autenticado del endpoint dinámico y del formulario de findings.
- Validación visual aceptada por el usuario.

## Validación de preflight de publicación

`publication_preflight.sh` debe validarse con:

- `bash -n publication_preflight.sh`.
- Ejecución directa `./publication_preflight.sh`.
- Security audit.
- Validadores de documentación/proyecto.
- `git diff --check` y `git diff --cached --check`.\n\n## Detalles Auditorías/Findings

Cobertura añadida: `DetailViewsTests` valida login requerido, render de detalle de auditoría, render de detalle de finding y enlaces Ver desde listados.\n

### 2026-06-17 — Validación cierre detalles Auditorías/Findings

Validaciones ejecutadas para cierre `v0.2.6-pre`:

- Build Docker.
- `python manage.py check`.
- `python manage.py makemigrations --check --dry-run`.
- Suite `core`: 35 tests OK.
- Security audit.
- Validadores de documentación y proyecto.
- `git diff --check`.
- Smoke HTTP autenticado de `audit_detail` y `finding_detail`.
- Validación de enlaces `Ver` desde listados.
- Validación visual aceptada por el usuario.

## Checks seguros planificados

Cobertura prevista/ejecutada: `SafeCheckPlanningTests` valida que solo se puedan planificar checks sobre activos auditables vinculados a la auditoría, que los checks intrusivos queden bloqueados y que el código de esta capa no contenga primitivas de ejecución técnica (`subprocess`, `os.system`, `requests`, `socket`).

<!-- AUDITORSECSUITE_SAFE_CHECKS_7A_VALIDATION_20260617 -->
### Evidencia de validación — checks seguros planificados sin ejecución real

Fecha: 2026-06-17.

Bloque funcional cerrado: catálogo y planificación de checks seguros, sin ejecución técnica.

Evidencias ejecutadas:

- Web recuperada y saludable: `/health/` respondió 200 tras rebuild con espera robusta.
- Migración aplicada: `core.0002_checkdefinition_auditcheckplan`.
- `python manage.py check`: OK.
- `python manage.py makemigrations --check --dry-run`: OK.
- `python manage.py test core.tests.SafeCheckPlanningTests -v 2`: 5 tests OK.
- `python manage.py test core -v 2`: 40 tests OK.
- Auditoría anti-ejecución: sin `subprocess`, `os.system`, `Popen`, `requests.` ni `socket.` en modelos/forms/views/templates del bloque.
- Security audit: `OK_SECURITY_AUDIT=1`.
- Validadores documentales/proyecto: `OK_DOCUMENTATION_ALIGNMENT=1` y `OK_PROJECT_ALIGNMENT=1`.
- Smoke funcional autenticado:
  - listado de checks: HTTP 200.
  - formulario de check: HTTP 200.
  - formulario de planificación: HTTP 200.
  - creación de check declarativo: HTTP 302.
  - planificación de check: HTTP 302.
  - detalle de auditoría: HTTP 200.
  - el detalle muestra “Checks planificados”, nombre y código del check.
  - `FINDINGS_BEFORE=3` y `FINDINGS_AFTER=3`.
  - `NO_AUTOMATIC_FINDINGS_CREATED=1`.
  - `NO_ENGINE_EXECUTION_TRIGGERED=1`.
  - `SMOKE_CLEANUP_OK=1`, sin residuos de smoke.

Conclusión: la capa queda validada como planificación declarativa/controlada, sin motor real, sin red, sin comandos y sin creación automática de findings.

### Bloque 8A — pruebas de catálogo inicial de checks seguros

El seed del catálogo debe validarse mediante migración de datos, tests específicos del catálogo, `makemigrations --check --dry-run`, suite `core`, auditoría anti-ejecución y smoke autenticado de listado/planificación.

<!-- AUDITORSECSUITE_SAFE_CHECK_CATALOG_8A_VALIDATION_20260617 -->
### Evidencia de validación — Bloque 8A catálogo inicial de checks seguros

Fecha: 2026-06-17.

Resultado validado:

- Migración de datos: `core.0003_seed_initial_safe_check_definitions`.
- Catálogo inicial sembrado: 10 checks.
- Todos los checks iniciales son manuales: `engine_key=manual`.
- Todos los checks iniciales son pasivos: `nivel_riesgo_operativo=passive`.
- Todos los checks iniciales están activos y requieren autorización.
- `INTRUSIVE_COUNT=0`.
- `NON_MANUAL_COUNT=0`.
- `DISABLED_COUNT=0`.
- `NO_AUTH_REQUIRED_COUNT=0`.
- `python manage.py check`: OK.
- `python manage.py makemigrations --check --dry-run`: OK.
- `SafeCheckCatalogSeedTests`: 3 tests OK.
- `SafeCheckPlanningTests`: 5 tests OK.
- Suite `core`: 43 tests OK.
- Auditoría anti-ejecución: sin `subprocess`, `os.system`, `Popen`, `requests.` ni `socket.` en código del bloque.
- Security audit: `OK_SECURITY_AUDIT=1`.
- Validadores documentales/proyecto: `OK_DOCUMENTATION_ALIGNMENT=1` y `OK_PROJECT_ALIGNMENT=1`.
- Smoke autenticado con check sembrado:
  - listado de checks muestra el catálogo.
  - planificación con `tls-certificate-manual-review`: OK.
  - detalle de auditoría muestra el check planificado.
  - no se crean findings automáticos.
  - no se ejecutan motores.

Conclusión: el catálogo inicial queda validado como base declarativa segura para planificación, sin ejecución técnica.
