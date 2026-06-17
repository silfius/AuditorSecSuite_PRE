# SPEC_002_PUBLIC_REPO_HARDENING — AuditorSecSuite_PRE

## Objetivo

Endurecer el repositorio público para que los cambios mantengan validaciones mínimas de calidad, seguridad, documentación y control de publicación.

## Alcance

- CI público.
- SECURITY raíz.
- LICENSE conservadora.
- Plantillas de PR e issues.
- Política de commits mínimos.
- Criterio crítico ante decisiones propuestas.

## Fuera de alcance

- Branch protection estricta.
- Releases.
- Publicación de imágenes Docker.
- Integración de motores de escaneo.

## Criterios de aceptación

- Validaciones locales OK.
- publication_preflight.sh OK con código de salida real.
- gitleaks OK.
- trufflehog OK.
- GitHub Actions OK tras push.
