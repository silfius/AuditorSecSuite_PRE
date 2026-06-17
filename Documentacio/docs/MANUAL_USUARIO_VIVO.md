# MANUAL_USUARIO_VIVO — AuditorSecSuite_PRE

Manual inicial. URL prevista http://<LAN_IP>:58780/. Secciones: Inicio, Activos, Auditorías, Findings, Admin. Capturas pendientes.

## Activos — alta y edición de activos

Desde `Activos` se puede consultar el inventario interno, crear nuevos activos y editar activos existentes.

El campo `Autorizado` debe marcarse únicamente cuando el activo sea propio o exista autorización explícita para auditarlo.

Pendiente de captura: pantalla del listado de activos con activos autorizados y no autorizados.
Pendiente de captura: pantalla del formulario de alta/edición de activo.

### Validación visual UX 1

La interfaz de `Activos` se ha mejorado visualmente tras revisión: listado con acción principal, tabla refinada, chips semánticos y formulario en tarjeta con estructura más clara.

Pendiente de incorporar capturas definitivas si se decide generar documentación visual completa.

## Auditorías con activos autorizados

Desde `Auditorías` se puede crear o editar una auditoría seleccionando únicamente activos auditables.

Un activo auditable debe estar activo y autorizado. Los activos no autorizados o inactivos no aparecen como seleccionables y se rechazan también en validación server-side.

Pendiente de captura: listado de auditorías.
Pendiente de captura: formulario de alta/edición de auditoría.

## Findings manuales vinculados

Desde `Findings` se puede crear o editar un hallazgo manual vinculado a una auditoría y a un activo perteneciente a esa auditoría.

El sistema valida en servidor que el activo seleccionado forme parte de la auditoría. Este flujo no ejecuta motores automáticos.

Pendiente de captura: listado de findings.
Pendiente de captura: formulario de alta/edición de finding.

## Selector dinámico de activos en Findings

Al crear o editar un finding, al escoger la auditoría se carga el listado de activos auditables vinculados a esa auditoría. Si la auditoría no tiene activos auditables, el selector lo indica.

Pendiente de captura: formulario de finding con selector de activos cargado dinámicamente.

### Findings — selector dinámico validado `v0.2.4-pre`

- En el formulario de alta/edición de findings, primero debe seleccionarse la auditoría.
- Después, el campo Activo se recarga con los activos auditables vinculados a esa auditoría.
- Si la auditoría no tiene activos auditables, el formulario muestra un mensaje informativo.
- Validación visual aceptada el 2026-06-17.

**Capturas pendientes para documentación final:**
- [ ] Captura del formulario antes de seleccionar auditoría.
- [ ] Captura del selector de activos cargado tras seleccionar auditoría.
