# DECISIONES_Y_ERRORES — AuditorSecSuite_PRE

Decisiones: uso personal/interno, no SaaS, no producto comercial, no reinventar motores, todo objetivo debe ser propio/autorizado, findings revisables manualmente.

## Error corregido — publication_preflight sin código de error real

Se detectó que `publication_preflight.sh` podía mostrar `STOP_PUBLICATION_PREFLIGHT=1` sin devolver estado de error al bloque llamador. Queda corregido para que todo STOP devuelva error y bloquee commits o pushes posteriores cuando proceda.

## Decisión — licencia conservadora inicial

Aunque el repositorio sea público, se mantiene `All rights reserved` hasta decidir explícitamente una licencia open source. Esto evita conceder permisos de copia, modificación o distribución por omisión.

## Decisión — commits mínimos y criterio crítico

Se establece que los commits deben ser estrictamente necesarios y no producirse por cada cambio menor. Se prioriza agrupar cambios en unidades revisables, validadas y con sentido funcional o de seguridad.

También se establece que el asistente debe actuar de forma crítica ante las decisiones propuestas por el usuario: no debe validar automáticamente una decisión si existe una alternativa más segura, mantenible, sencilla o técnicamente superior.

## Finding manual antes de motores

Antes de integrar motores técnicos se implementan findings manuales revisables. Esto permite consolidar auditoría, activo, severidad, estado y recomendación sin depender de resultados automáticos ni ejecutar acciones técnicas.

## 2026-06-17 — Preflight raíz canónico

Se detectó un falso bloqueo tras commit porque el bloque de cierre invocó `./publication_preflight.sh` y el fichero no existía en raíz. Se decide crear ese wrapper como ruta canónica, manteniendo dentro las comprobaciones de seguridad, documentación, proyecto y whitespace.

## Decisión — checks planificados antes de motores reales

Antes de integrar motores técnicos reales se implementa una capa de catálogo y planificación de checks. Esta decisión reduce riesgo operativo, mantiene la trazabilidad y evita introducir ejecución técnica prematura.

<!-- AUDITORSECSUITE_SAFE_CHECKS_7A_VALIDATION_20260617_OPERACION -->
### Nota operativa — contenedor sin bind mount de código

Durante el bloque de checks seguros se confirmó que el servicio `app` usa `COPY app /app` en la imagen y no un bind mount del código fuente. Por tanto, después de modificar código en el host, Django dentro del contenedor no ve los cambios hasta ejecutar `docker compose up -d --build app`.

También queda como cautela operativa no imprimir `docker compose config` completo en salidas compartidas, porque puede exponer valores procedentes de `.env`.

### Decisión — catálogo inicial como migración de datos

El catálogo inicial de checks seguros se implementa como migración de datos para que sea reproducible en cualquier entorno y en la base de test. No se usa carga manual puntual ni script operativo aislado.

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
