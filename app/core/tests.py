from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import ActivoForm
from .models import Activo, Auditoria, Finding
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
