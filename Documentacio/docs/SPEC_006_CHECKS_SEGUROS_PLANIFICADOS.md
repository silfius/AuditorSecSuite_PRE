# SPEC_006 — Checks seguros planificados sin ejecución

## Objetivo

Crear una capa declarativa para definir y planificar checks técnicos sobre auditorías y activos autorizados, sin ejecutar motores reales.

## Alcance incluido

- Catálogo de checks seguros.
- Planificación de checks por auditoría y activo.
- Validación server-side de que el activo pertenece a la auditoría.
- Validación server-side de que el activo sigue siendo auditable.
- Bloqueo de checks intrusivos.
- Visualización en detalle de auditoría.

## Fuera de alcance

- Ejecución de motores.
- Llamadas de red.
- `subprocess`, comandos shell o Docker exec.
- Generación automática de findings.
- Integración con testssl, SSLyze, Nuclei, ZAP o Greenbone.

## Criterio de seguridad

La planificación es una intención operativa, no una ejecución técnica. Cualquier futura integración de motor deberá crear un bloque independiente con guardarraíles adicionales, logs, autorización explícita y validaciones negativas.
