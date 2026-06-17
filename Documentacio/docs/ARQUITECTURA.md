# ARQUITECTURA — AuditorSecSuite_PRE

Stack Docker-first con Django y PostgreSQL. Modelos iniciales: Activo, Auditoria, AuditoriaActivo, Finding. Motores futuros aislados: testssl/SSLyze, Nuclei, ZAP, Greenbone.

## Inventario de activos

El inventario utiliza `Activo`, `ActivoForm`, `asset_list`, `asset_create` y `asset_update`. La autorización del activo se mantiene como guardarraíl funcional antes de cualquier futura ejecución de motores.

## Base visual mínima

La interfaz mantiene CSS propio en `core/base.html` como base inicial: página con cabecera, toolbar, botones, tarjetas, tablas, formularios en grid, avisos y chips semánticos. Es una solución ligera previa a decidir si conviene extraer CSS estático o adoptar un sistema de diseño externo.

## Auditorías con activos autorizados

`AuditoriaForm` filtra activos auditables y valida server-side que solo se vinculen activos con `Activo.puede_auditarse()`. La relación se persiste mediante `AuditoriaActivo`.

## Findings manuales

`FindingForm` valida server-side que el activo seleccionado esté vinculado a la auditoría mediante `AuditoriaActivo`. No ejecuta motores ni genera findings automáticos.

## Selector dinámico auditoría-activo en Findings

El formulario de Findings usa un endpoint autenticado para cargar dinámicamente los activos auditables de la auditoría seleccionada. La validación server-side de `FindingForm` sigue siendo la autoridad funcional.
