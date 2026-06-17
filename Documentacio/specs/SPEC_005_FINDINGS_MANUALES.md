# SPEC_005_FINDINGS_MANUALES — AuditorSecSuite_PRE

## Objetivo

Implementar el flujo web de alta y edición de findings manuales vinculados a una auditoría y a un activo incluido en esa auditoría.

El finding es un hallazgo revisable manualmente. En este bloque no se generan findings mediante motores automáticos.

## Regla funcional canónica

- Un finding debe pertenecer a una auditoría.
- Un finding debe estar vinculado a un activo.
- El activo seleccionado debe estar vinculado previamente a la auditoría mediante `AuditoriaActivo`.
- El servidor debe rechazar un POST manipulado que intente vincular el finding a un activo fuera de la auditoría.
- El flujo no ejecuta escaneos ni acciones técnicas sobre el activo.

## Alcance funcional

- Listado de findings con auditoría, activo, severidad y estado.
- Alta de finding manual desde interfaz web.
- Edición de finding existente.
- Selección de auditoría.
- Selección de activo filtrada por la auditoría seleccionada o validada server-side.
- Campos de título, descripción, recomendación, severidad, estado y herramienta/origen si aplica.
- Vista protegida por login.

## Fuera de alcance

- Integración con Nuclei, ZAP, Greenbone, testssl.sh u otros motores.
- Importación automática de resultados.
- Evidencias adjuntas o ficheros de prueba.
- Exportación de informes.
- Workflow avanzado de aprobación/cierre.

## Riesgos

- Registrar findings sobre activos no incluidos en la auditoría.
- Confundir un finding manual con un resultado automático validado por herramienta.
- Empezar a guardar evidencias sensibles antes de definir política de almacenamiento.
- Exponer detalles sensibles en un repositorio público o en documentación versionada.

## Criterios de aceptación

- Usuario autenticado puede listar findings.
- Usuario autenticado puede crear finding manual.
- Usuario autenticado puede editar finding manual.
- El formulario no debe aceptar activos que no estén vinculados a la auditoría.
- Un POST manipulado con activo externo a la auditoría debe producir formulario inválido.
- Tests cubren login requerido, creación, edición y rechazo de activo no vinculado.
- No se ejecuta ningún escaneo real.

## Validaciones previstas

- Django check.
- makemigrations check.
- tests core.
- smoke HTTP autenticado de listado/alta.
- security_audit.sh.
- publication_preflight.sh antes de push público.
