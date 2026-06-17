# PUBLICACION — AuditorSecSuite_PRE

## Regla principal

El repositorio puede ser público solo si supera un preflight específico de publicación.

## Condiciones obligatorias antes de push público

- `security_audit.sh`: OK.
- `publication_preflight.sh`: OK.
- `gitleaks`: OK.
- `trufflehog`: OK.
- Sin `.env` real versionado.
- Sin tokens, claves, certificados, dumps, logs, storage ni evidencias reales.
- Sin rutas internas reales del servidor.
- Sin IP LAN real del servidor en documentación o ejemplos públicos.
- Sin informes reales de auditoría.
- Sin datos de clientes, empresa o terceros.

## Alcance público

El repositorio público contiene código, documentación técnica genérica y plantillas. No contiene datos operativos reales.

## Herramienta dual-use

Este proyecto puede orquestar herramientas de auditoría. Su uso queda limitado a activos propios o con autorización explícita.
