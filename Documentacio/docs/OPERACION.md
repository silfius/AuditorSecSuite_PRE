# OPERACION — AuditorSecSuite_PRE

Runtime: docker compose --env-file .env up -d --build. URLs: /health/, /app/, /app/activos/, /app/auditorias/, /app/findings/, /admin/. Puerto 58780.

## Publicación controlada

Antes de publicar commits en `main`, debe ejecutarse desde la raíz del repositorio:

`./publication_preflight.sh`

Este wrapper es la ruta canónica de preflight. No deben invocarse rutas alternativas salvo que se documente expresamente una migración del procedimiento.

<!-- AUDITORSECSUITE_SAFE_CHECKS_7A_VALIDATION_20260617_OPERACION -->
### Nota operativa — contenedor sin bind mount de código

Durante el bloque de checks seguros se confirmó que el servicio `app` usa `COPY app /app` en la imagen y no un bind mount del código fuente. Por tanto, después de modificar código en el host, Django dentro del contenedor no ve los cambios hasta ejecutar `docker compose up -d --build app`.

También queda como cautela operativa no imprimir `docker compose config` completo en salidas compartidas, porque puede exponer valores procedentes de `.env`.
