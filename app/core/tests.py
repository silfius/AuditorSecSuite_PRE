from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import ActivoForm, AuditoriaForm
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
