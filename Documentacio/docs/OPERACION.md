# OPERACION — AuditorSecSuite_PRE

Runtime: docker compose --env-file .env up -d --build. URLs: /health/, /app/, /app/activos/, /app/auditorias/, /app/findings/, /admin/. Puerto 58780.

## Publicación controlada

Antes de publicar commits en `main`, debe ejecutarse desde la raíz del repositorio:

`./publication_preflight.sh`

Este wrapper es la ruta canónica de preflight. No deben invocarse rutas alternativas salvo que se documente expresamente una migración del procedimiento.
