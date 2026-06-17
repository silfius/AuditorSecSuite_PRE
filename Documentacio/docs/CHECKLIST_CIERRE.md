# CHECKLIST_CIERRE — AuditorSecSuite_PRE

Cierre: alcance claro, seguridad, validación técnica, validación funcional, documentación viva, git diff check, tests según riesgo y registro de pendientes reales.

## Commits mínimos

- Confirmar que el commit representa una unidad significativa.
- Evitar commits de microcambios salvo que sean puntos de restauración necesarios.
- Antes de commitear, validar que el cambio merece trazabilidad propia.

## Preflight de publicación

Para cierres con commit y push:

- [ ] Working tree limpio salvo `.env` ignorado.
- [ ] `python manage.py check`.
- [ ] `python manage.py makemigrations --check --dry-run`.
- [ ] Tests según riesgo.
- [ ] `./publication_preflight.sh`.
- [ ] `git push origin main`.
- [ ] CI verificado.
