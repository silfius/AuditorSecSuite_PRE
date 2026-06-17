# CHANGELOG — AuditorSecSuite_PRE

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
