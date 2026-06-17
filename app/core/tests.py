from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
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
            valor="192.168.1.253",
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
