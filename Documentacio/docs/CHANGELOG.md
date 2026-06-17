# CHANGELOG — AuditorSecSuite_PRE

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
