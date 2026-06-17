# Generated manually for AuditorSecSuite_PRE safe check catalog seed.

from django.db import migrations


INITIAL_SAFE_CHECKS = [{'codigo': 'tls-certificate-manual-review', 'nombre': 'Revisión manual de certificado TLS', 'descripcion': 'Check declarativo para revisar caducidad, emisor, CN/SAN y coherencia del certificado. No conecta al activo ni ejecuta herramientas.', 'categoria': 'tls', 'engine_key': 'manual', 'tipo_activo_aplicable': 'web,domain', 'nivel_riesgo_operativo': 'passive'}, {'codigo': 'tls-protocol-policy-review', 'nombre': 'Revisión manual de política TLS', 'descripcion': 'Check declarativo para documentar protocolo mínimo esperado, uso de HTTPS y requisitos internos. No realiza handshake ni escaneo.', 'categoria': 'tls', 'engine_key': 'manual', 'tipo_activo_aplicable': 'web', 'nivel_riesgo_operativo': 'passive'}, {'codigo': 'http-security-headers-manual-review', 'nombre': 'Revisión manual de cabeceras HTTP de seguridad', 'descripcion': 'Check declarativo para revisar CSP, HSTS, X-Frame-Options, Referrer-Policy y cabeceras relacionadas a partir de evidencias aportadas. No hace peticiones HTTP.', 'categoria': 'http', 'engine_key': 'manual', 'tipo_activo_aplicable': 'web', 'nivel_riesgo_operativo': 'passive'}, {'codigo': 'http-cookie-flags-manual-review', 'nombre': 'Revisión manual de flags de cookies', 'descripcion': 'Check declarativo para revisar Secure, HttpOnly y SameSite en cookies a partir de evidencias manuales. No inspecciona tráfico ni automatiza navegador.', 'categoria': 'http', 'engine_key': 'manual', 'tipo_activo_aplicable': 'web', 'nivel_riesgo_operativo': 'passive'}, {'codigo': 'dns-public-records-inventory', 'nombre': 'Inventario manual de registros DNS públicos', 'descripcion': 'Check declarativo para documentar A/AAAA/CNAME/NS/TXT relevantes cuando el auditor aporta la evidencia. No consulta DNS automáticamente.', 'categoria': 'dns', 'engine_key': 'manual', 'tipo_activo_aplicable': 'domain', 'nivel_riesgo_operativo': 'passive'}, {'codigo': 'dns-email-authentication-review', 'nombre': 'Revisión manual SPF/DKIM/DMARC', 'descripcion': 'Check declarativo para revisar configuración de autenticación de correo a partir de evidencias aportadas. No consulta registros DNS.', 'categoria': 'dns', 'engine_key': 'manual', 'tipo_activo_aplicable': 'domain', 'nivel_riesgo_operativo': 'passive'}, {'codigo': 'web-login-surface-manual-review', 'nombre': 'Revisión manual de superficie de login', 'descripcion': 'Check declarativo para revisar existencia de login, MFA, mensajes de error y exposición funcional a partir de revisión manual autorizada. No automatiza credenciales.', 'categoria': 'web', 'engine_key': 'manual', 'tipo_activo_aplicable': 'web', 'nivel_riesgo_operativo': 'passive'}, {'codigo': 'web-exposed-admin-manual-review', 'nombre': 'Revisión manual de paneles administrativos expuestos', 'descripcion': 'Check declarativo para registrar si existen paneles administrativos expuestos según evidencia manual. No fuerza rutas ni enumera directorios.', 'categoria': 'web', 'engine_key': 'manual', 'tipo_activo_aplicable': 'web', 'nivel_riesgo_operativo': 'passive'}, {'codigo': 'infra-exposed-services-manual-review', 'nombre': 'Revisión manual de servicios expuestos', 'descripcion': 'Check declarativo para documentar servicios/puertos expuestos cuando la evidencia procede de inventario autorizado. No ejecuta escaneo de puertos.', 'categoria': 'infra', 'engine_key': 'manual', 'tipo_activo_aplicable': 'ip,host', 'nivel_riesgo_operativo': 'passive'}, {'codigo': 'internal-availability-evidence-review', 'nombre': 'Revisión manual de evidencia de disponibilidad', 'descripcion': 'Check declarativo para registrar estado de disponibilidad observado o comunicado. No ejecuta ping, curl ni comprobación externa.', 'categoria': 'internal', 'engine_key': 'manual', 'tipo_activo_aplicable': 'web,domain,ip,host', 'nivel_riesgo_operativo': 'passive'}]


def seed_initial_safe_checks(apps, schema_editor):
    CheckDefinition = apps.get_model("core", "CheckDefinition")

    for item in INITIAL_SAFE_CHECKS:
        defaults = {
            "nombre": item["nombre"],
            "descripcion": item["descripcion"],
            "categoria": item["categoria"],
            "engine_key": item["engine_key"],
            "tipo_activo_aplicable": item["tipo_activo_aplicable"],
            "is_enabled": True,
            "nivel_riesgo_operativo": item["nivel_riesgo_operativo"],
            "requiere_autorizacion": True,
        }
        CheckDefinition.objects.update_or_create(
            codigo=item["codigo"],
            defaults=defaults,
        )


def unseed_initial_safe_checks(apps, schema_editor):
    CheckDefinition = apps.get_model("core", "CheckDefinition")
    CheckDefinition.objects.filter(
        codigo__in=[item["codigo"] for item in INITIAL_SAFE_CHECKS],
        audit_plans__isnull=True,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_checkdefinition_auditcheckplan"),
    ]

    operations = [
        migrations.RunPython(seed_initial_safe_checks, unseed_initial_safe_checks),
    ]
