# CHANGELOG — AuditorSecSuite_PRE

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
