# INDICE_TECNICO — AuditorSecSuite_PRE

Docs vivos en Documentacio/docs. Código: app/core/models.py, views.py, tests.py, templates. Runtime: auditorsecsuite_pre_app y auditorsecsuite_pre_db.

- `PUBLICACION.md`: política de publicación pública y preflight.

## Hardening público

- `SPEC_002_PUBLIC_REPO_HARDENING.md`: endurecimiento del repositorio público.
- `.github/pull_request_template.md`: plantilla de pull request.
- `.github/ISSUE_TEMPLATE/`: plantillas de issues.

- `SPEC_003_INVENTARIO_ACTIVOS_AUTORIZADOS.md`: inventario inicial de activos autorizados.

- `SPEC_004_AUDITORIAS_ACTIVOS_AUTORIZADOS.md`: auditorías vinculadas solo a activos auditables.

- `SPEC_005_FINDINGS_MANUALES.md`: findings manuales vinculados a auditoría y activo de la auditoría.

- `SPEC_006_CHECKS_SEGUROS_PLANIFICADOS.md`: catálogo y planificación de checks seguros sin ejecución.

- `app/core/migrations/0003_seed_initial_safe_check_definitions.py`: seed declarativo del catálogo inicial de checks seguros.

- `CheckDefinition.applies_to_asset()`: normaliza alias de tipo de activo y decide aplicabilidad de checks.
- `SafeCheckApplicabilityTests`: pruebas de aplicabilidad por tipo de activo.
