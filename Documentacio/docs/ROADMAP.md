# ROADMAP — AuditorSecSuite_PRE

Fase 0 foundation. Fase 1 inventario y checks seguros. Fase 2 ZAP web. Fase 3 Greenbone infraestructura. Fase 4 reporting interno y retest.

## Bloque funcional 1 — inventario de activos autorizados

Primer bloque funcional real tras el hardening público. Debe crear una base segura para registrar activos antes de integrar cualquier motor de análisis.

## Bloque funcional 2 — auditorías con activos autorizados

Crear alta/edición de auditorías seleccionando exclusivamente activos auditables. No se integran motores técnicos en este bloque.

## Bloque funcional 3 — findings manuales

Crear alta/edición de findings manuales vinculados a una auditoría y a activos pertenecientes a esa auditoría. No se integran motores automáticos.

### 2026-06-17 — Bloque cerrado: selector dinámico Findings

- Cerrada la mejora UX/funcional que vincula dinámicamente auditoría y activos en el formulario de findings.
- Siguiente evolución natural: mejorar detalle de auditoría/finding y preparar checks controlados sin ejecución real no autorizada.\n\n### 2026-06-17 — Bloque 6A en curso: detalles operativos

Se avanza en detalle de auditorías y findings antes de diseñar checks/motores controlados. Objetivo: mejorar trazabilidad funcional sin añadir ejecución técnica.\n

### 2026-06-17 — Bloque cerrado: detalles operativos

Cerrado el detalle operativo de auditorías y findings. El proyecto queda preparado para estudiar el siguiente paso: checks controlados, simulados o motores seguros, siempre sobre auditorías y activos autorizados.

### 2026-06-17 — Bloque 7A — checks seguros planificados

Se inicia la capa de checks seguros sin ejecución. El objetivo es definir y planificar controles técnicos de forma declarativa antes de integrar cualquier motor real.

### 2026-06-17 — Bloque 8A en curso: catálogo inicial de checks seguros

Se avanza en catálogo declarativo de checks manuales/pasivos antes de cualquier integración de motores. La fase sigue siendo planificación segura: no hay ejecución técnica.
