# MANUAL_USUARIO_VIVO — AuditorSecSuite_PRE

Manual inicial. URL prevista http://<LAN_IP>:58780/. Secciones: Inicio, Activos, Auditorías, Findings, Admin. Capturas pendientes.

## Activos — alta y edición de activos

Desde `Activos` se puede consultar el inventario interno, crear nuevos activos y editar activos existentes.

El campo `Autorizado` debe marcarse únicamente cuando el activo sea propio o exista autorización explícita para auditarlo.

Pendiente de captura: pantalla del listado de activos con activos autorizados y no autorizados.
Pendiente de captura: pantalla del formulario de alta/edición de activo.

### Validación visual UX 1

La interfaz de `Activos` se ha mejorado visualmente tras revisión: listado con acción principal, tabla refinada, chips semánticos y formulario en tarjeta con estructura más clara.

Pendiente de incorporar capturas definitivas si se decide generar documentación visual completa.

## Auditorías con activos autorizados

Desde `Auditorías` se puede crear o editar una auditoría seleccionando únicamente activos auditables.

Un activo auditable debe estar activo y autorizado. Los activos no autorizados o inactivos no aparecen como seleccionables y se rechazan también en validación server-side.

Pendiente de captura: listado de auditorías.
Pendiente de captura: formulario de alta/edición de auditoría.

## Findings manuales vinculados

Desde `Findings` se puede crear o editar un hallazgo manual vinculado a una auditoría y a un activo perteneciente a esa auditoría.

El sistema valida en servidor que el activo seleccionado forme parte de la auditoría. Este flujo no ejecuta motores automáticos.

Pendiente de captura: listado de findings.
Pendiente de captura: formulario de alta/edición de finding.

## Selector dinámico de activos en Findings

Al crear o editar un finding, al escoger la auditoría se carga el listado de activos auditables vinculados a esa auditoría. Si la auditoría no tiene activos auditables, el selector lo indica.

Pendiente de captura: formulario de finding con selector de activos cargado dinámicamente.

### Findings — selector dinámico validado `v0.2.4-pre`

- En el formulario de alta/edición de findings, primero debe seleccionarse la auditoría.
- Después, el campo Activo se recarga con los activos auditables vinculados a esa auditoría.
- Si la auditoría no tiene activos auditables, el formulario muestra un mensaje informativo.
- Validación visual aceptada el 2026-06-17.

**Capturas pendientes para documentación final:**
- [ ] Captura del formulario antes de seleccionar auditoría.
- [ ] Captura del selector de activos cargado tras seleccionar auditoría.\n\n## Detalle de auditorías y findings

Pendiente de revisión visual.

- Desde el listado de auditorías, la acción Ver abre el detalle de la auditoría.
- El detalle de auditoría muestra datos principales, activos vinculados y findings asociados.
- Desde el listado de findings, la acción Ver abre el detalle del finding.
- El detalle de finding muestra auditoría, activo, severidad, estado, descripción, evidencia y recomendación.

**Capturas pendientes:**
- [ ] Detalle de auditoría.
- [ ] Detalle de finding.\n

### Detalle de auditorías y findings validado `v0.2.6-pre`

- Desde el listado de auditorías, la acción **Ver** abre el detalle de la auditoría.
- El detalle de auditoría muestra perfil, estado, usuario creador, alcance, activos vinculados y findings asociados.
- Los activos vinculados se distinguen entre **Auditable** y **No auditable actualmente**.
- Desde el listado de findings, la acción **Ver** abre el detalle del finding.
- El detalle de finding muestra auditoría, activo, severidad, estado, herramienta/origen, descripción, evidencia, recomendación y referencia.
- Validación visual aceptada el 2026-06-17.

**Capturas pendientes para documentación final:**
- [ ] Listado de auditorías con acción Ver.
- [ ] Detalle de auditoría.
- [ ] Listado de findings con acción Ver.
- [ ] Detalle de finding.

## Checks seguros planificados

Desde `Checks` se puede mantener un catálogo declarativo de checks técnicos seguros. Estos checks no ejecutan motores ni realizan acciones técnicas.

Desde el detalle de una auditoría se pueden planificar checks sobre los activos vinculados y actualmente auditables.

**Capturas pendientes:**
- [ ] Listado de checks seguros.
- [ ] Formulario de check seguro.
- [ ] Detalle de auditoría con checks planificados.
- [ ] Formulario de planificación de check.

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

### Catálogo inicial de checks seguros

El sistema incorpora un catálogo inicial de checks manuales y pasivos para planificar revisiones habituales en auditorías autorizadas. Estos checks no ejecutan herramientas ni realizan consultas técnicas: solo sirven para preparar y ordenar el trabajo.

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

### Aplicabilidad de checks

Al planificar checks en una auditoría, el sistema filtra y valida los checks según el tipo de activo. Esto evita planificar revisiones DNS sobre activos web tipo URL o revisiones HTTP sobre dominios cuando no correspondan.

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
