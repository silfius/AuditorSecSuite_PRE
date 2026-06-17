# DECISIONES_Y_ERRORES — AuditorSecSuite_PRE

Decisiones: uso personal/interno, no SaaS, no producto comercial, no reinventar motores, todo objetivo debe ser propio/autorizado, findings revisables manualmente.

## Error corregido — publication_preflight sin código de error real

Se detectó que `publication_preflight.sh` podía mostrar `STOP_PUBLICATION_PREFLIGHT=1` sin devolver estado de error al bloque llamador. Queda corregido para que todo STOP devuelva error y bloquee commits o pushes posteriores cuando proceda.

## Decisión — licencia conservadora inicial

Aunque el repositorio sea público, se mantiene `All rights reserved` hasta decidir explícitamente una licencia open source. Esto evita conceder permisos de copia, modificación o distribución por omisión.

## Decisión — commits mínimos y criterio crítico

Se establece que los commits deben ser estrictamente necesarios y no producirse por cada cambio menor. Se prioriza agrupar cambios en unidades revisables, validadas y con sentido funcional o de seguridad.

También se establece que el asistente debe actuar de forma crítica ante las decisiones propuestas por el usuario: no debe validar automáticamente una decisión si existe una alternativa más segura, mantenible, sencilla o técnicamente superior.
