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
