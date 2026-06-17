# SPEC_003_INVENTARIO_ACTIVOS_AUTORIZADOS — AuditorSecSuite_PRE

## Objetivo

Construir el primer flujo funcional del proyecto: inventario web de activos auditables con control explícito de autorización antes de cualquier ejecución técnica.

## Alcance funcional

- Listado interno de activos.
- Alta y edición básica de activos.
- Campo obligatorio de autorización.
- Estado activo/inactivo.
- Tipos iniciales: host, url, dominio, servicio y contenedor.
- Vista protegida por login.
- Mensajes visibles si un activo no está autorizado.

## Fuera de alcance

- Ejecución de escaneos reales.
- Integración con Nuclei, ZAP, Greenbone, testssl.sh u otros motores.
- Reportes técnicos avanzados.
- Multiusuario avanzado o roles finos.

## Riesgos

- Registrar objetivos no autorizados.
- Confundir inventario con permiso de escaneo.
- Exponer datos internos en repositorio público.
- Empezar a integrar motores antes de tener guardarraíles funcionales.

## Criterios de aceptación

- Un usuario autenticado puede ver el listado de activos.
- Un usuario autenticado puede crear y editar activos.
- La autorización queda explícita y visible.
- Ninguna acción futura de auditoría podrá ejecutarse sobre activos no autorizados.
- Tests de modelo/vista cubren activos autorizados y no autorizados.
- No se introducen datos reales en fixtures, docs ni repositorio.

## Validaciones previstas

- Django check.
- makemigrations check.
- tests core selectivos.
- security_audit.sh.
- publication_preflight.sh antes de push público.
- CI GitHub tras push.
