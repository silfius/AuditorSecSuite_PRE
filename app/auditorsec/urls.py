from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from core import views

urlpatterns = [
    path("", lambda request: redirect("/app/")),
    path("health/", views.health, name="health"),
    path("app/", views.dashboard, name="dashboard"),
    path("app/activos/", views.asset_list, name="asset_list"),
    path("app/auditorias/", views.audit_list, name="audit_list"),
    path("app/findings/", views.finding_list, name="finding_list"),
    path("admin/", admin.site.urls),
]
