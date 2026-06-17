# TESTING — AuditorSecSuite_PRE

Un cambio no está validado sin evidencia. Validaciones: compose config, Django check, makemigrations check, tests por riesgo, git diff check, security audit. Tests no ejecutarán escaneos reales.

## Inventario de activos autorizados

Cobertura prevista/ejecutada: `AssetFormTests`, `AssetViewsTests` y pruebas de modelo para asegurar que un activo solo es auditable si está activo y autorizado.

## Auditorías con activos autorizados

Cobertura prevista/ejecutada: `AuditFormTests` y `AuditViewsTests` para validar login requerido, creación, edición y rechazo de activos no auditables.

## Findings manuales

Cobertura prevista/ejecutada: `FindingFormTests` y `FindingViewsTests` para validar login requerido, creación, edición y rechazo de activos no vinculados a la auditoría.
