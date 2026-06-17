from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import ActivoForm, AuditoriaForm, FindingForm
from .models import Activo, Auditoria, AuditoriaActivo, Finding
from .version import APPLICATION_VERSION


class HealthTests(TestCase):
    def test_health_ok(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")


class VersionTests(TestCase):
    def test_version_explicit(self):
        self.assertRegex(APPLICATION_VERSION, r"^\d+\.\d+\.\d+")


class CoreModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="auditor", password="unused")
        self.asset = Activo.objects.create(
            nombre="Servidor PRE",
            tipo=Activo.Tipo.HOST,
            valor="example.test",
            entorno="LAN",
            autorizado=True,
        )
        self.audit = Auditoria.objects.create(
            nombre="Auditoría inicial interna",
            alcance="Servidor propio autorizado.",
            perfil=Auditoria.Perfil.INVENTARIO,
            creado_por=self.user,
        )

    def test_finding_creation(self):
        finding = Finding.objects.create(
            auditoria=self.audit,
            activo=self.asset,
            titulo="Servicio expuesto pendiente de revisión",
            severidad=Finding.Severidad.MEDIA,
            descripcion="Hallazgo de prueba controlado.",
        )
        self.assertIn("Servicio expuesto", str(finding))

    def test_asset_can_be_audited_only_when_active_and_authorized(self):
        self.assertTrue(self.asset.puede_auditarse())
        self.asset.autorizado = False
        self.assertFalse(self.asset.puede_auditarse())
        self.asset.autorizado = True
        self.asset.activo = False
        self.assertFalse(self.asset.puede_auditarse())


class AssetFormTests(TestCase):
    def test_asset_form_strips_text_fields(self):
        form = ActivoForm(data={
            "nombre": "  Web interna  ",
            "tipo": Activo.Tipo.URL,
            "valor": "  https://example.test  ",
            "entorno": "  PRE  ",
            "autorizado": "on",
            "activo": "on",
            "notas": "",
        })
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["nombre"], "Web interna")
        self.assertEqual(form.cleaned_data["valor"], "https://example.test")
        self.assertEqual(form.cleaned_data["entorno"], "PRE")


class AuthenticatedViewsTests(TestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_authenticated(self):
        user = get_user_model().objects.create_user(username="viewer", password="unused")
        self.client.force_login(user)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AuditorSecSuite")


class AssetViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="asset-user", password="unused")

    def test_asset_list_requires_login(self):
        response = self.client.get(reverse("asset_list"))
        self.assertEqual(response.status_code, 302)

    def test_asset_create_requires_login(self):
        response = self.client.get(reverse("asset_create"))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_create_authorized_asset(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("asset_create"), data={
            "nombre": "Web corporativa",
            "tipo": Activo.Tipo.URL,
            "valor": "https://example.test",
            "entorno": "PRE",
            "autorizado": "on",
            "activo": "on",
            "notas": "Activo de prueba controlado.",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Activo.objects.filter(nombre="Web corporativa", autorizado=True).exists())
        self.assertContains(response, "Autorizado")

    def test_authenticated_user_can_create_unauthorized_asset_with_warning(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("asset_create"), data={
            "nombre": "Dominio pendiente",
            "tipo": Activo.Tipo.DOMINIO,
            "valor": "pending.example.test",
            "entorno": "PRE",
            "activo": "on",
            "notas": "Pendiente de autorización.",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        asset = Activo.objects.get(nombre="Dominio pendiente")
        self.assertFalse(asset.autorizado)
        self.assertFalse(asset.puede_auditarse())
        self.assertContains(response, "No autorizado")

    def test_authenticated_user_can_update_asset_authorization(self):
        asset = Activo.objects.create(
            nombre="Host pendiente",
            tipo=Activo.Tipo.HOST,
            valor="host-pending.example.test",
            entorno="PRE",
            autorizado=False,
            activo=True,
        )
        self.client.force_login(self.user)
        response = self.client.post(reverse("asset_update", args=[asset.pk]), data={
            "nombre": "Host pendiente",
            "tipo": Activo.Tipo.HOST,
            "valor": "host-pending.example.test",
            "entorno": "PRE",
            "autorizado": "on",
            "activo": "on",
            "notas": "Autorizado tras revisión.",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        asset.refresh_from_db()
        self.assertTrue(asset.autorizado)
        self.assertTrue(asset.puede_auditarse())


class AuditFormTests(TestCase):
    def setUp(self):
        self.perfil_value = Auditoria._meta.get_field("perfil").choices[0][0]
        self.estado_value = Auditoria._meta.get_field("estado").choices[0][0]
        self.authorized = Activo.objects.create(
            nombre="Activo autorizado",
            tipo=Activo.Tipo.URL,
            valor="https://audit-ok.example.test",
            entorno="PRE",
            autorizado=True,
            activo=True,
        )
        self.unauthorized = Activo.objects.create(
            nombre="Activo no autorizado",
            tipo=Activo.Tipo.URL,
            valor="https://audit-no.example.test",
            entorno="PRE",
            autorizado=False,
            activo=True,
        )
        self.inactive = Activo.objects.create(
            nombre="Activo inactivo",
            tipo=Activo.Tipo.URL,
            valor="https://audit-inactive.example.test",
            entorno="PRE",
            autorizado=True,
            activo=False,
        )

    def test_audit_form_only_lists_auditable_assets(self):
        form = AuditoriaForm()
        self.assertIn(self.authorized, form.fields["activos"].queryset)
        self.assertNotIn(self.unauthorized, form.fields["activos"].queryset)
        self.assertNotIn(self.inactive, form.fields["activos"].queryset)

    def test_audit_form_rejects_unauthorized_asset_post(self):
        form = AuditoriaForm(data={
            "nombre": "Auditoría manipulada",
            "alcance": "Intento de vinculación no autorizada.",
            "perfil": self.perfil_value,
            "estado": self.estado_value,
            "activos": [str(self.unauthorized.pk)],
        })
        self.assertFalse(form.is_valid())

    def test_audit_form_rejects_inactive_asset_post(self):
        form = AuditoriaForm(data={
            "nombre": "Auditoría manipulada inactiva",
            "alcance": "Intento de vinculación inactiva.",
            "perfil": self.perfil_value,
            "estado": self.estado_value,
            "activos": [str(self.inactive.pk)],
        })
        self.assertFalse(form.is_valid())


class AuditViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="audit-user", password="unused")
        self.perfil_value = Auditoria._meta.get_field("perfil").choices[0][0]
        estado_choices = list(Auditoria._meta.get_field("estado").choices)
        self.estado_value = estado_choices[0][0]
        self.alt_estado_value = estado_choices[1][0] if len(estado_choices) > 1 else estado_choices[0][0]
        self.authorized = Activo.objects.create(
            nombre="Activo auditable",
            tipo=Activo.Tipo.URL,
            valor="https://audit-view-ok.example.test",
            entorno="PRE",
            autorizado=True,
            activo=True,
        )
        self.unauthorized = Activo.objects.create(
            nombre="Activo no auditable",
            tipo=Activo.Tipo.URL,
            valor="https://audit-view-no.example.test",
            entorno="PRE",
            autorizado=False,
            activo=True,
        )

    def test_audit_list_requires_login(self):
        response = self.client.get(reverse("audit_list"))
        self.assertEqual(response.status_code, 302)

    def test_audit_create_requires_login(self):
        response = self.client.get(reverse("audit_create"))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_create_audit_with_authorized_asset(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("audit_create"), data={
            "nombre": "Auditoría web interna",
            "alcance": "Revisión controlada sin motor técnico.",
            "perfil": self.perfil_value,
            "estado": self.estado_value,
            "activos": [str(self.authorized.pk)],
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        audit = Auditoria.objects.get(nombre="Auditoría web interna")
        self.assertEqual(audit.auditoria_activos.count(), 1)
        self.assertTrue(AuditoriaActivo.objects.filter(auditoria=audit, activo=self.authorized).exists())
        self.assertContains(response, "Auditoría web interna")

    def test_authenticated_user_cannot_create_audit_with_unauthorized_asset(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("audit_create"), data={
            "nombre": "Auditoría no permitida",
            "alcance": "Intento manipulado.",
            "perfil": self.perfil_value,
            "estado": self.estado_value,
            "activos": [str(self.unauthorized.pk)],
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Auditoria.objects.filter(nombre="Auditoría no permitida").exists())

    def test_authenticated_user_can_update_audit_assets(self):
        audit = Auditoria.objects.create(
            nombre="Auditoría editable",
            alcance="Alcance inicial.",
            perfil=self.perfil_value,
            estado=self.estado_value,
            creado_por=self.user,
        )
        self.client.force_login(self.user)
        response = self.client.post(reverse("audit_update", args=[audit.pk]), data={
            "nombre": "Auditoría editable",
            "alcance": "Alcance actualizado.",
            "perfil": self.perfil_value,
            "estado": self.alt_estado_value,
            "activos": [str(self.authorized.pk)],
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        audit.refresh_from_db()
        self.assertEqual(audit.estado, self.alt_estado_value)
        self.assertEqual(audit.auditoria_activos.count(), 1)


class FindingFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="finding-form-user", password="unused")
        self.audit = Auditoria.objects.create(
            nombre="Auditoría findings",
            alcance="Alcance findings.",
            perfil=Auditoria._meta.get_field("perfil").choices[0][0],
            estado=Auditoria._meta.get_field("estado").choices[0][0],
            creado_por=self.user,
        )
        self.linked_asset = Activo.objects.create(
            nombre="Activo en auditoría",
            tipo=Activo.Tipo.URL,
            valor="https://finding-linked.example.test",
            entorno="PRE",
            autorizado=True,
            activo=True,
        )
        self.external_asset = Activo.objects.create(
            nombre="Activo externo",
            tipo=Activo.Tipo.URL,
            valor="https://finding-external.example.test",
            entorno="PRE",
            autorizado=True,
            activo=True,
        )
        AuditoriaActivo.objects.create(auditoria=self.audit, activo=self.linked_asset)

    def finding_payload(self, activo):
        data = {
            "auditoria": str(self.audit.pk),
            "activo": str(activo.pk),
            "titulo": "Cabecera de seguridad ausente",
            "severidad": Finding._meta.get_field("severidad").choices[0][0],
            "estado": Finding._meta.get_field("estado").choices[0][0],
        }
        field_names = {field.name for field in Finding._meta.fields}
        if "descripcion" in field_names:
            data["descripcion"] = "Descripción manual del hallazgo."
        if "recomendacion" in field_names:
            data["recomendacion"] = "Aplicar cabecera de seguridad correspondiente."
        if "herramienta" in field_names:
            data["herramienta"] = "Manual"
        return data

    def test_finding_form_accepts_asset_linked_to_audit(self):
        form = FindingForm(data=self.finding_payload(self.linked_asset))
        self.assertTrue(form.is_valid(), form.errors)

    def test_finding_form_rejects_asset_not_linked_to_audit(self):
        form = FindingForm(data=self.finding_payload(self.external_asset))
        self.assertFalse(form.is_valid())
        self.assertIn("activo", form.errors)


class FindingViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="finding-view-user", password="unused")
        self.audit = Auditoria.objects.create(
            nombre="Auditoría finding vista",
            alcance="Alcance finding vista.",
            perfil=Auditoria._meta.get_field("perfil").choices[0][0],
            estado=Auditoria._meta.get_field("estado").choices[0][0],
            creado_por=self.user,
        )
        self.linked_asset = Activo.objects.create(
            nombre="Activo finding vinculado",
            tipo=Activo.Tipo.URL,
            valor="https://finding-view-linked.example.test",
            entorno="PRE",
            autorizado=True,
            activo=True,
        )
        self.external_asset = Activo.objects.create(
            nombre="Activo finding externo",
            tipo=Activo.Tipo.URL,
            valor="https://finding-view-external.example.test",
            entorno="PRE",
            autorizado=True,
            activo=True,
        )
        AuditoriaActivo.objects.create(auditoria=self.audit, activo=self.linked_asset)

    def finding_payload(self, activo, title="Finding manual vista"):
        data = {
            "auditoria": str(self.audit.pk),
            "activo": str(activo.pk),
            "titulo": title,
            "severidad": Finding._meta.get_field("severidad").choices[0][0],
            "estado": Finding._meta.get_field("estado").choices[0][0],
        }
        field_names = {field.name for field in Finding._meta.fields}
        if "descripcion" in field_names:
            data["descripcion"] = "Descripción manual del finding."
        if "recomendacion" in field_names:
            data["recomendacion"] = "Recomendación manual."
        if "herramienta" in field_names:
            data["herramienta"] = "Manual"
        return data

    def test_finding_list_requires_login(self):
        response = self.client.get(reverse("finding_list"))
        self.assertEqual(response.status_code, 302)

    def test_finding_create_requires_login(self):
        response = self.client.get(reverse("finding_create"))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_create_manual_finding(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("finding_create"),
            data=self.finding_payload(self.linked_asset),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Finding.objects.filter(titulo="Finding manual vista", activo=self.linked_asset, auditoria=self.audit).exists())
        self.assertContains(response, "Finding manual vista")

    def test_authenticated_user_cannot_create_finding_for_external_asset(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("finding_create"),
            data=self.finding_payload(self.external_asset, title="Finding externo no permitido"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Finding.objects.filter(titulo="Finding externo no permitido").exists())

    def test_authenticated_user_can_update_manual_finding(self):
        finding = Finding.objects.create(
            auditoria=self.audit,
            activo=self.linked_asset,
            titulo="Finding editable",
            severidad=Finding._meta.get_field("severidad").choices[0][0],
            estado=Finding._meta.get_field("estado").choices[0][0],
        )
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("finding_update", args=[finding.pk]),
            data=self.finding_payload(self.linked_asset, title="Finding editado"),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        finding.refresh_from_db()
        self.assertEqual(finding.titulo, "Finding editado")


class FindingDynamicAssetSelectorTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="finding-selector-user", password="unused")
        self.audit = Auditoria.objects.create(
            nombre="Auditoría selector dinámico",
            alcance="Alcance selector dinámico.",
            perfil=Auditoria._meta.get_field("perfil").choices[0][0],
            estado=Auditoria._meta.get_field("estado").choices[0][0],
            creado_por=self.user,
        )
        self.linked_asset = Activo.objects.create(
            nombre="Activo selector vinculado",
            tipo=Activo.Tipo.URL,
            valor="https://selector-linked.example.test",
            entorno="PRE",
            autorizado=True,
            activo=True,
        )
        self.external_asset = Activo.objects.create(
            nombre="Activo selector externo",
            tipo=Activo.Tipo.URL,
            valor="https://selector-external.example.test",
            entorno="PRE",
            autorizado=True,
            activo=True,
        )
        self.unauthorized_asset = Activo.objects.create(
            nombre="Activo selector no autorizado",
            tipo=Activo.Tipo.URL,
            valor="https://selector-unauthorized.example.test",
            entorno="PRE",
            autorizado=False,
            activo=True,
        )
        AuditoriaActivo.objects.create(auditoria=self.audit, activo=self.linked_asset)
        AuditoriaActivo.objects.create(auditoria=self.audit, activo=self.unauthorized_asset)

    def test_finding_audit_assets_endpoint_requires_login(self):
        response = self.client.get(reverse("finding_audit_assets", args=[self.audit.pk]))
        self.assertEqual(response.status_code, 302)

    def test_finding_audit_assets_endpoint_returns_only_linked_auditable_assets(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("finding_audit_assets", args=[self.audit.pk]))
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        asset_ids = {item["id"] for item in payload["assets"]}

        self.assertIn(self.linked_asset.pk, asset_ids)
        self.assertNotIn(self.external_asset.pk, asset_ids)
        self.assertNotIn(self.unauthorized_asset.pk, asset_ids)

    def test_finding_create_form_contains_dynamic_selector_hook(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("finding_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "data-assets-url-template")
        self.assertContains(response, "/app/findings/auditorias/0/activos/")
        self.assertContains(response, "loadAssets")

class DetailViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="detail-user", password="unused")
        self.audit = Auditoria.objects.create(
            nombre="Auditoría detalle",
            alcance="Alcance de detalle.",
            perfil=Auditoria._meta.get_field("perfil").choices[0][0],
            estado=Auditoria._meta.get_field("estado").choices[0][0],
            creado_por=self.user,
        )
        self.linked_asset = Activo.objects.create(
            nombre="Activo detalle vinculado",
            tipo=Activo.Tipo.URL,
            valor="https://detail-linked.example.test",
            entorno="PRE",
            autorizado=True,
            activo=True,
        )
        self.unauthorized_asset = Activo.objects.create(
            nombre="Activo detalle no autorizado",
            tipo=Activo.Tipo.URL,
            valor="https://detail-unauthorized.example.test",
            entorno="PRE",
            autorizado=False,
            activo=True,
        )
        AuditoriaActivo.objects.create(auditoria=self.audit, activo=self.linked_asset)
        AuditoriaActivo.objects.create(auditoria=self.audit, activo=self.unauthorized_asset)
        self.finding = Finding.objects.create(
            auditoria=self.audit,
            activo=self.linked_asset,
            titulo="Finding detalle",
            severidad=Finding._meta.get_field("severidad").choices[0][0],
            estado=Finding._meta.get_field("estado").choices[0][0],
            herramienta="Manual",
            descripcion="Descripción detalle",
            evidencia="Evidencia detalle",
            recomendacion="Recomendación detalle",
            referencia="REF-DET",
        )

    def test_audit_detail_requires_login(self):
        response = self.client.get(reverse("audit_detail", args=[self.audit.pk]))
        self.assertEqual(response.status_code, 302)

    def test_finding_detail_requires_login(self):
        response = self.client.get(reverse("finding_detail", args=[self.finding.pk]))
        self.assertEqual(response.status_code, 302)

    def test_audit_detail_shows_assets_and_findings(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("audit_detail", args=[self.audit.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Auditoría detalle")
        self.assertContains(response, "Activo detalle vinculado")
        self.assertContains(response, "Activo detalle no autorizado")
        self.assertContains(response, "Auditable")
        self.assertContains(response, "No auditable actualmente")
        self.assertContains(response, "Finding detalle")

    def test_finding_detail_shows_context(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("finding_detail", args=[self.finding.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Finding detalle")
        self.assertContains(response, "Auditoría detalle")
        self.assertContains(response, "Activo detalle vinculado")
        self.assertContains(response, "Descripción detalle")
        self.assertContains(response, "Recomendación detalle")

    def test_lists_include_detail_links(self):
        self.client.force_login(self.user)

        audit_response = self.client.get(reverse("audit_list"))
        self.assertEqual(audit_response.status_code, 200)
        self.assertContains(audit_response, reverse("audit_detail", args=[self.audit.pk]))

        finding_response = self.client.get(reverse("finding_list"))
        self.assertEqual(finding_response.status_code, 200)
        self.assertContains(finding_response, reverse("finding_detail", args=[self.finding.pk]))



from datetime import date as _safe_date
from pathlib import Path as _SafePath
from uuid import uuid4 as _safe_uuid4
from django.contrib.auth import get_user_model as _safe_get_user_model
from django.core.exceptions import ValidationError as _SafeValidationError
from django.db import models as _safe_django_models
from django.urls import reverse as _safe_reverse
from .models import CheckDefinition, AuditCheckPlan
from .forms import AuditCheckPlanForm


_SAFE_CORE_DIR = _SafePath(__file__).resolve().parent



class SafeCheckCatalogSeedTests(TestCase):
    def test_initial_safe_check_catalog_is_seeded(self):
        expected_codes = {
            "tls-certificate-manual-review",
            "tls-protocol-policy-review",
            "http-security-headers-manual-review",
            "http-cookie-flags-manual-review",
            "dns-public-records-inventory",
            "dns-email-authentication-review",
            "web-login-surface-manual-review",
            "web-exposed-admin-manual-review",
            "infra-exposed-services-manual-review",
            "internal-availability-evidence-review",
        }

        found_codes = set(
            CheckDefinition.objects.filter(codigo__in=expected_codes).values_list("codigo", flat=True)
        )

        self.assertEqual(found_codes, expected_codes)

    def test_initial_safe_check_catalog_is_non_intrusive_and_manual(self):
        seeded = CheckDefinition.objects.filter(
            codigo__in=[
                "tls-certificate-manual-review",
                "tls-protocol-policy-review",
                "http-security-headers-manual-review",
                "http-cookie-flags-manual-review",
                "dns-public-records-inventory",
                "dns-email-authentication-review",
                "web-login-surface-manual-review",
                "web-exposed-admin-manual-review",
                "infra-exposed-services-manual-review",
                "internal-availability-evidence-review",
            ]
        )

        self.assertEqual(seeded.count(), 10)
        self.assertFalse(
            seeded.filter(nivel_riesgo_operativo=CheckDefinition.RISK_INTRUSIVE).exists()
        )
        self.assertFalse(
            seeded.exclude(engine_key=CheckDefinition.ENGINE_MANUAL).exists()
        )
        self.assertFalse(seeded.filter(is_enabled=False).exists())
        self.assertFalse(seeded.filter(requiere_autorizacion=False).exists())

    def test_check_list_shows_seeded_catalog(self):
        user = get_user_model().objects.create_user(
            username="safe-catalog-test-user",
            password="test-pass-12345",
        )
        self.client.force_login(user)
        response = self.client.get(reverse("core_check_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Revisión manual de certificado TLS")
        self.assertContains(response, "http-security-headers-manual-review")


class SafeCheckPlanningTests(TestCase):
    def setUp(self):
        self.user = _safe_get_user_model().objects.create_user(
            username=f"user-{_safe_uuid4().hex[:8]}",
            password="test-pass-12345",
        )
        self.client.force_login(self.user)

        self.asset = self._create_instance(Activo, "asset")
        self._force_asset_auditable(self.asset)

        self.audit = self._create_instance(Auditoria, "audit")
        AuditoriaActivo.objects.create(auditoria=self.audit, activo=self.asset)

        self.check_definition = CheckDefinition.objects.create(
            codigo=f"tls-expiry-{_safe_uuid4().hex[:8]}",
            nombre="Caducidad de certificado TLS",
            descripcion="Check declarativo sin ejecución técnica.",
            categoria=CheckDefinition.CATEGORY_TLS,
            engine_key=CheckDefinition.ENGINE_MANUAL,
            nivel_riesgo_operativo=CheckDefinition.RISK_PASSIVE,
            is_enabled=True,
        )

    def _field_value(self, field, prefix):
        if getattr(field, "choices", None):
            for value, _label in field.choices:
                if value not in ("", None):
                    return value

        if isinstance(field, (_safe_django_models.CharField, _safe_django_models.SlugField)):
            return f"{prefix}-{field.name}-{_safe_uuid4().hex[:8]}"[: field.max_length or 80]
        if isinstance(field, _safe_django_models.TextField):
            return f"{prefix}-{field.name}"
        if isinstance(field, _safe_django_models.BooleanField):
            return True
        if isinstance(field, _safe_django_models.DateTimeField):
            from django.utils import timezone
            return timezone.now()
        if isinstance(field, _safe_django_models.DateField):
            return _safe_date.today()
        if isinstance(field, _safe_django_models.IntegerField):
            return 1
        return None

    def _create_instance(self, model, prefix):
        data = {}
        for field in model._meta.fields:
            if field.auto_created or field.primary_key:
                continue
            if field.has_default() or field.null or field.blank:
                continue
            if isinstance(field, _safe_django_models.ForeignKey):
                if field.remote_field.model == _safe_get_user_model():
                    data[field.name] = self.user
                continue
            value = self._field_value(field, prefix)
            if value is not None:
                data[field.name] = value
        return model.objects.create(**data)

    def _force_asset_auditable(self, asset):
        for field in asset._meta.fields:
            if isinstance(field, _safe_django_models.BooleanField):
                setattr(asset, field.name, True)
        asset.save()
        self.assertTrue(asset.puede_auditarse())

    def test_plan_requires_asset_linked_to_audit(self):
        other_asset = self._create_instance(Activo, "other")
        self._force_asset_auditable(other_asset)

        plan = AuditCheckPlan(
            auditoria=self.audit,
            activo=other_asset,
            check_definition=self.check_definition,
        )

        with self.assertRaises(_SafeValidationError):
            plan.full_clean()

    def test_plan_rejects_non_auditable_asset(self):
        changed = False
        for field in self.asset._meta.fields:
            if isinstance(field, _safe_django_models.BooleanField):
                setattr(self.asset, field.name, False)
                changed = True
                break

        if not changed:
            self.skipTest("Activo no tiene booleanos para forzar no auditable.")

        self.asset.save()

        if self.asset.puede_auditarse():
            self.skipTest("No se pudo forzar un activo no auditable con el esquema actual.")

        plan = AuditCheckPlan(
            auditoria=self.audit,
            activo=self.asset,
            check_definition=self.check_definition,
        )

        with self.assertRaises(_SafeValidationError):
            plan.full_clean()

    def test_intrusive_checks_are_not_plannable(self):
        intrusive = CheckDefinition.objects.create(
            codigo=f"intrusive-{_safe_uuid4().hex[:8]}",
            nombre="Check intrusivo bloqueado",
            categoria=CheckDefinition.CATEGORY_INFRA,
            engine_key=CheckDefinition.ENGINE_NOOP,
            nivel_riesgo_operativo=CheckDefinition.RISK_INTRUSIVE,
            is_enabled=True,
        )

        form = AuditCheckPlanForm(
            data={
                "check_definition": intrusive.pk,
                "activo": self.asset.pk,
                "estado": AuditCheckPlan.STATE_PLANNED,
                "motivo_bloqueo": "",
            },
            auditoria=self.audit,
        )

        self.assertFalse(form.is_valid())

    def test_authenticated_user_can_create_safe_check_plan(self):
        url = _safe_reverse("core_audit_check_plan_create", args=[self.audit.pk])
        response = self.client.post(
            url,
            {
                "check_definition": self.check_definition.pk,
                "activo": self.asset.pk,
                "estado": AuditCheckPlan.STATE_PLANNED,
                "motivo_bloqueo": "",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            AuditCheckPlan.objects.filter(
                auditoria=self.audit,
                activo=self.asset,
                check_definition=self.check_definition,
            ).exists()
        )

    def test_safe_check_layer_has_no_execution_primitives(self):
        source = "\n".join(
            [
                (_SAFE_CORE_DIR / "models.py").read_text(encoding="utf-8"),
                (_SAFE_CORE_DIR / "forms.py").read_text(encoding="utf-8"),
                (_SAFE_CORE_DIR / "views.py").read_text(encoding="utf-8"),
            ]
        )

        for fragment in ["subprocess.", "Popen(", "os.system(", "requests.", "socket."]:
            self.assertNotIn(fragment, source)
