# CHANGELOG — AuditorSecSuite_PRE

## v0.2.7-pre — checks seguros planificados

### Añadido
- Añadido catálogo declarativo de checks seguros.
- Añadida planificación de checks por auditoría y activo.
- Añadida sección de checks planificados en el detalle de auditoría.
- Añadida especificación `SPEC_006_CHECKS_SEGUROS_PLANIFICADOS.md`.

### Seguridad
- No se ejecutan motores técnicos.
- No se realizan llamadas de red.
- No se invocan comandos shell ni `subprocess`.
- Solo se permite planificar checks sobre activos vinculados a la auditoría y actualmente auditables.
- Los checks intrusivos quedan bloqueados en esta fase.

### Validación
- Pendiente de cierre del bloque.


## v0.2.6-pre — detalle operativo de auditorías y findings

### Añadido
- Añadidas vistas de detalle para auditorías y findings.
- Añadidas rutas `audit_detail` y `finding_detail`.
- Añadidos templates `audit_detail.html` y `finding_detail.html`.
- Añadida acción `Ver` en listados de auditorías y findings.
- El detalle de auditoría muestra datos principales, activos vinculados y findings asociados.
- El detalle de finding muestra auditoría, activo, severidad, estado, origen, descripción, evidencia, recomendación y referencia.

### Seguridad
- Las vistas de detalle mantienen `login_required`.
- Las pantallas son informativas y no ejecutan motores técnicos.
- El detalle de auditoría conserva trazabilidad mostrando activos vinculados aunque actualmente ya no sean auditables, diferenciándolos visualmente.

### Validación
- Build Docker OK.
- `manage.py check` OK.
- `makemigrations --check --dry-run` OK.
- `python manage.py test core`: 35 tests OK.
- Security audit OK.
- Validadores de documentación/proyecto OK.
- `git diff --check` OK.
- Smoke HTTP autenticado de `audit_detail` y `finding_detail` OK.
- Enlaces `Ver` desde listados OK.
- Revisión visual aceptada por el usuario el 2026-06-17.

## v0.2.5-pre — preflight canónico de publicación

### Añadido
- Añadido wrapper canónico raíz `./publication_preflight.sh`.
- El cierre de bloques publicados debe ejecutar siempre este wrapper antes de `git push`.
- El wrapper valida working tree limpio, ficheros sensibles básicos, security audit, alineación documental/proyecto y whitespace.

### Corregido
- Evitado el falso bloqueo producido por invocar un preflight inexistente en raíz.

### Validación
- `bash -n publication_preflight.sh` OK.
- `./publication_preflight.sh` OK.
- `manage.py check` OK.
- `makemigrations --check --dry-run` OK.
- `python manage.py test core` OK.
- Security audit OK.
- Validadores de documentación/proyecto OK.
- CI GitHub pendiente tras push.

## v0.2.4-pre — selector dinámico de activos en Findings

### Mejorado
- Añadido selector dinámico de activos en el formulario de findings.
- Al seleccionar una auditoría, el formulario carga únicamente los activos auditables vinculados a esa auditoría.
- Añadido endpoint autenticado `/app/findings/auditorias/<id>/activos/`.
- Añadido JS en `finding_form.html` para recargar el desplegable de activos sin abandonar el formulario.

### Seguridad
- El endpoint solo devuelve activos activos, autorizados y vinculados a la auditoría.
- La validación server-side de `FindingForm` sigue siendo la autoridad funcional.
- No se ejecutan motores reales ni automatismos ofensivos.

### Validación
- Build Docker OK.
- `manage.py check` OK.
- `makemigrations --check --dry-run` OK.
- `python manage.py test core`: 30 tests OK.
- Security audit OK.
- Validadores de documentación/proyecto OK.
- `git diff --check` OK.
- Smoke HTTP autenticado del selector dinámico OK.
- Revisión visual aceptada por el usuario el 2026-06-17.

## v0.2.3-pre — findings manuales vinculados

### Añadido
- `SPEC_005_FINDINGS_MANUALES.md`.
- Alta y edición de findings manuales desde interfaz web.
- `FindingForm` con validación server-side de auditoría y activo.
- Rutas `/app/findings/nuevo/` y `/app/findings/<id>/editar/`.
- Tests `FindingFormTests` y `FindingViewsTests`.

### Seguridad
- Un finding solo puede vincularse a un activo incluido en la auditoría correspondiente.
- El servidor rechaza activos externos a la auditoría aunque se manipule el POST.
- No se ejecutan motores reales ni se importan resultados automáticos en este bloque.

### Validación
- `manage.py check` OK.
- `makemigrations --check --dry-run` OK.
- `python manage.py test core`: 27 tests OK.
- Smoke HTTP autenticado de findings OK.
- Revisión visual aceptada por usuario.

## v0.2.2-pre — auditorías con activos autorizados

### Añadido
- `SPEC_004_AUDITORIAS_ACTIVOS_AUTORIZADOS.md`.
- Alta y edición de auditorías desde interfaz web.
- `AuditoriaForm` con selección múltiple de activos auditables.
- Rutas `/app/auditorias/nueva/` y `/app/auditorias/<id>/editar/`.
- Tests `AuditFormTests` y `AuditViewsTests`.

### Seguridad
- Solo se pueden vincular activos con `Activo.puede_auditarse()`.
- El servidor rechaza activos no autorizados o inactivos aunque se manipule el POST.
- No se ejecutan motores reales en este bloque.

### Validación
- `manage.py check` OK.
- `makemigrations --check --dry-run` OK.
- `python manage.py test core`: 20 tests OK.
- Smoke HTTP autenticado de auditorías OK.
- Revisión visual aceptable.

## v0.2.1-pre — mejora visual de activos

### Mejorado
- Base visual inicial en `core/base.html`: cabecera, layout, botones, tarjetas, tablas, formularios y chips semánticos.
- Listado de activos con acción principal, empty state y estados visuales más claros.
- Formulario de activos con card, grid, ayudas y controles de autorización más legibles.

### Validación
- Validación técnica OK.
- Smoke HTTP UX OK.
- Revisión visual del usuario: mejora aceptada.

## v0.2.0-pre — inventario de activos autorizados

### Añadido
- Alta y edición de activos desde interfaz web.
- `ActivoForm` para normalizar campos de inventario.
- Guardarraíl funcional `Activo.puede_auditarse()`.
- Tests de formulario, vistas autenticadas, creación, edición y autorización.
- `SPEC_003_INVENTARIO_ACTIVOS_AUTORIZADOS.md`.

### Seguridad
- Los activos no autorizados quedan visibles como no aptos para auditoría.
- No se integran motores de escaneo en este bloque.

## v0.1.6-pre — plantillas públicas y premisas operativas

### Añadido
- Plantilla de pull request.
- Plantillas de issue para bugs y specs.
- `SPEC_002_PUBLIC_REPO_HARDENING.md`.
- Premisa de commits estrictamente necesarios.
- Premisa de criterio crítico ante decisiones propuestas.

### Decisión
- Se agrupan estos cambios en un único commit de cierre de hardening público, evitando microcommits documentales.

## v0.1.5-pre — LICENSE raíz conservadora

### Añadido
- `LICENSE` raíz con reserva de derechos.

### Decisión
- El repositorio es público, pero no se concede todavía licencia open source.

## v0.1.4-pre — contrato real de publication preflight

### Corregido
- `publication_preflight.sh` ahora devuelve código de error cuando detecta `STOP_PUBLICATION_PREFLIGHT=1`.

### Seguridad
- Se evita que una publicación continúe si el preflight muestra fallo lógico.

## v0.1.3-pre — SECURITY raíz

### Añadido
- `SECURITY.md` raíz para el repositorio público.

### Seguridad
- Se explicita el uso dual controlado y la prohibición de publicar secretos, evidencias reales o datos de terceros.

### Límites
- No se añaden todavía plantillas de issue/PR.
- No se añade todavía licencia raíz.
- No se activa branch protection.

## v0.1.2-pre — CI público mínimo

### Añadido
- Workflow público `.github/workflows/ci.yml`.
- Validación CI con Django check, migraciones, tests, validadores documentales, `security_audit.sh`, `gitleaks` y `trufflehog`.

### Límites
- No se activa todavía branch protection.
- No se añaden todavía plantillas de issue/PR ni licencia.
- No se integran motores de escaneo.

## v0.1.1-pre — publicación pública controlada

### Añadido
- Política de publicación pública en `Documentacio/docs/PUBLICACION.md`.
- Script `Documentacio/scripts/publication_preflight.sh`.
- Preflight obligatorio con `gitleaks` y `trufflehog` antes de push público.

### Cambiado
- Saneadas referencias públicas a IP LAN real y ruta interna del servidor.
- Versión visible actualizada a `0.1.1-pre`.

### Seguridad
- `.env.example` queda permitido como plantilla sin secretos.
- `.env` real continúa ignorado y no versionado.
- Se bloquea publicación si aparecen rutas internas reales, IP LAN real, dumps, logs, storage o evidencias reales.

v0.1.0-pre — foundation inicial: scaffold Docker/Django/PostgreSQL, modelos base, documentación viva, specs y validadores. Sin escaneos ni publicación externa.

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

## v0.2.8-pre — catálogo inicial declarativo de checks seguros

### Añadido
- Migración de datos `core.0003_seed_initial_safe_check_definitions`.
- Catálogo inicial de 10 checks seguros, manuales y pasivos: TLS, cabeceras HTTP, cookies, DNS, autenticación de correo, superficie web, paneles administrativos expuestos, servicios expuestos y disponibilidad documentada.
- Tests específicos `SafeCheckCatalogSeedTests`.

### Seguridad
- Los checks sembrados son declarativos: `engine_key=manual`.
- No se ejecutan motores, red, comandos, escaneos ni peticiones HTTP/DNS.
- Todos los checks iniciales son no intrusivos y requieren autorización.

### Validación
- Pendiente de completar en el cierre del bloque 8A.

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
