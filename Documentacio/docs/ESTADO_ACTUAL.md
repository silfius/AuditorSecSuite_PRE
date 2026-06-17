# ESTADO_ACTUAL — AuditorSecSuite_PRE

Proyecto iniciado: AuditorSecSuite_PRE. Ruta /opt/AuditorSecSuite_PRE. Versión 0.1.0-pre. Objetivo: suite interna de auditoría técnica. Bloque activo: foundation. No ejecuta escaneos todavía.

## Siguiente bloque funcional — Inventario de activos autorizados

Se inicia el diseño del primer flujo funcional: inventario de activos con autorización explícita. No se integran motores de escaneo en este bloque.

## Bloque funcional 1F — implementación inicial de inventario

Se implementa alta y edición de activos con autorización explícita. No se integran motores de escaneo.

## UX 1 — mejora visual de activos

Tras revisión visual, se detecta que la interfaz inicial de activos era funcional pero demasiado básica. Se mejora listado y formulario con una base visual propia, botones, tarjetas, grid de formulario y chips semánticos.

### UX 1 aceptada visualmente

El usuario confirma que la nueva interfaz de activos mejora claramente respecto a la versión inicial. Queda pendiente aplicar el mismo criterio visual a futuros módulos cuando proceda.

## Siguiente bloque funcional — Auditorías con activos autorizados

Se prepara el diseño del flujo de auditorías vinculadas a activos auditables. El criterio de seguridad será `Activo.puede_auditarse()`.

## Bloque 2C — implementación de auditorías autorizadas

Se implementa alta y edición de auditorías vinculadas únicamente a activos auditables. No se ejecutan motores reales.

## Bloque 2D — cierre auditorías autorizadas

Alta y edición de auditorías quedan implementadas con selección exclusiva de activos auditables. La revisión visual resulta aceptable para continuar el proyecto. No se integran ni ejecutan motores reales.

## Siguiente bloque funcional — Findings manuales

Se prepara el diseño del flujo de findings manuales. Un finding debe vincularse a una auditoría y a un activo previamente incluido en esa auditoría.

## Bloque 3C — implementación de findings manuales

Se implementa alta y edición de findings manuales vinculados a auditoría y a activos pertenecientes a esa auditoría. No se ejecutan motores reales.

## Bloque 3D — cierre findings manuales

Alta y edición de findings manuales quedan implementadas y validadas. El usuario confirma revisión visual correcta. No se integran ni ejecutan motores reales.

## Bloque 4B — selector dinámico Findings

Se implementa carga dinámica de activos auditables al seleccionar auditoría en el formulario de Findings. El backend continúa validando la relación auditoría-activo.

## Bloque 4C — cierre selector dinámico Findings

El selector dinámico de activos en Findings queda validado técnica y visualmente. Al escoger una auditoría, el campo Activo carga únicamente activos auditables vinculados a esa auditoría. Versión de cierre: `v0.2.4-pre`.

## Bloque 5A — preflight canónico de publicación

Se normaliza el cierre de publicación creando `./publication_preflight.sh` como ruta canónica. El objetivo es evitar falsos bloqueos por rutas inexistentes y centralizar las comprobaciones antes de `git push`. Versión: `v0.2.5-pre`.\n\n## Bloque 6A.2 — detalle operativo Auditorías/Findings

Implementadas vistas de detalle para auditorías y findings, pendientes de revisión visual. El detalle de auditoría diferencia activos actualmente auditables y no auditables para mantener trazabilidad.\n

## Bloque 6A.3 — cierre detalle operativo Auditorías/Findings

El detalle operativo de auditorías y findings queda implementado, validado técnica y visualmente. Versión de cierre: `v0.2.6-pre`.

- Auditorías: detalle con datos principales, activos vinculados y findings asociados.
- Findings: detalle con contexto de auditoría, activo y campos descriptivos.
- No se ejecutan motores técnicos.
- Validación visual aceptada el 2026-06-17.

## Bloque 7A — checks seguros planificados

En curso la implementación de una capa declarativa de checks seguros. No ejecuta motores, no realiza llamadas de red y no genera findings automáticos.

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
