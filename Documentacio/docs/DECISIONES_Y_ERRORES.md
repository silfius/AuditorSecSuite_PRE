# DECISIONES_Y_ERRORES — AuditorSecSuite_PRE

Decisiones: uso personal/interno, no SaaS, no producto comercial, no reinventar motores, todo objetivo debe ser propio/autorizado, findings revisables manualmente.

## Error corregido — publication_preflight sin código de error real

Se detectó que `publication_preflight.sh` podía mostrar `STOP_PUBLICATION_PREFLIGHT=1` sin devolver estado de error al bloque llamador. Queda corregido para que todo STOP devuelva error y bloquee commits o pushes posteriores cuando proceda.

## Decisión — licencia conservadora inicial

Aunque el repositorio sea público, se mantiene `All rights reserved` hasta decidir explícitamente una licencia open source. Esto evita conceder permisos de copia, modificación o distribución por omisión.
