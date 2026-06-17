# SPEC_004_AUDITORIAS_ACTIVOS_AUTORIZADOS — AuditorSecSuite_PRE

## Objetivo

Crear el flujo web de alta y edición de auditorías vinculadas exclusivamente a activos auditables.

Un activo auditable es aquel que cumple `activo=True` y `autorizado=True`, usando `Activo.puede_auditarse()` como regla funcional canónica.

## Alcance funcional

- Listado de auditorías con número de activos vinculados.
- Alta de auditoría desde interfaz web.
- Edición de auditoría existente.
- Selección múltiple de activos auditables.
- Exclusión de activos no autorizados o inactivos en el formulario.
- Validación server-side para impedir vincular activos no auditables aunque se manipule el POST.
- Vista protegida por login.

## Fuera de alcance

- Ejecución de motores reales.
- Programación temporal de auditorías.
- Lanzamiento de Nuclei, ZAP, Greenbone, testssl.sh u otras herramientas.
- Gestión avanzada de permisos por usuario/rol.
- Resultados técnicos automáticos o findings generados por motor.

## Riesgos

- Vincular por error activos no autorizados.
- Confiar solo en el filtrado visual del formulario y olvidar validación server-side.
- Confundir creación de auditoría con permiso de ejecución técnica.
- Avanzar hacia motores reales sin haber cerrado los guardarraíles.

## Criterios de aceptación

- Usuario autenticado puede listar auditorías.
- Usuario autenticado puede crear auditoría.
- Usuario autenticado puede editar auditoría.
- Formulario solo muestra activos auditables.
- Manipular un POST con activo no autorizado debe producir formulario inválido.
- Manipular un POST con activo inactivo debe producir formulario inválido.
- Tests cubren creación, edición, login requerido y rechazo de activos no auditables.
- No se ejecuta ningún escaneo real.

## Validaciones previstas

- Django check.
- makemigrations check.
- tests core.
- smoke HTTP autenticado de listado/alta.
- security_audit.sh.
- publication_preflight.sh antes de push público.
