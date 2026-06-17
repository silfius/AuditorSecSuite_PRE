# INSTRUCCIONES_PROYECTO — AuditorSecSuite_PRE

Normas: bloques con objetivo y validación; no set -e; no exit 1; STOP=0/1; documentación viva; tests por riesgo; security_audit.sh antes de Git; solo activos propios o autorizados; uso personal/interno, no producto comercial.

## Commits estrictamente necesarios

No se debe crear un commit por cada cambio menor. Los commits deben reservarse para hitos relevantes: cierre de bloque funcional, cambio estructural, cambio de seguridad, publicación, corrección crítica o punto estable que tenga valor real como unidad de revisión/rollback.

Los cambios documentales menores, ajustes preparatorios y subpasos internos deben acumularse y validarse, pero no necesariamente commitearse hasta que formen una unidad significativa.

## Criterio crítico ante decisiones del usuario

Las propuestas del usuario no deben aceptarse automáticamente. Deben evaluarse con criterio técnico, funcional, de seguridad y mantenibilidad.

Se dará la razón al usuario cuando la propuesta sea correcta o cuando no exista una alternativa claramente mejor. Si existe una opción más segura, más simple, más robusta o más inteligente, debe proponerse y justificarse antes de ejecutar.

## Ruta canónica de preflight

La ruta canónica de preflight de publicación es `./publication_preflight.sh`, ejecutada desde la raíz del repositorio. Los bloques de cierre no deben llamar a un script inexistente ni asumir otra ubicación sin diagnóstico previo.
