# ARQUITECTURA — AuditorSecSuite_PRE

Stack Docker-first con Django y PostgreSQL. Modelos iniciales: Activo, Auditoria, AuditoriaActivo, Finding. Motores futuros aislados: testssl/SSLyze, Nuclei, ZAP, Greenbone.

## Inventario de activos

El inventario utiliza `Activo`, `ActivoForm`, `asset_list`, `asset_create` y `asset_update`. La autorización del activo se mantiene como guardarraíl funcional antes de cualquier futura ejecución de motores.
