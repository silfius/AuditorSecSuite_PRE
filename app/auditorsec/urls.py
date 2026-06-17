from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from core import views

urlpatterns = [
    path("", lambda request: redirect("/app/")),
    path("health/", views.health, name="health"),
    path("app/", views.dashboard, name="dashboard"),
    path("app/activos/", views.asset_list, name="asset_list"),
    path("app/activos/nuevo/", views.asset_create, name="asset_create"),
    path("app/activos/<int:pk>/editar/", views.asset_update, name="asset_update"),
    path("app/auditorias/", views.audit_list, name="audit_list"),
    path("app/auditorias/nueva/", views.audit_create, name="audit_create"),
    path("app/auditorias/<int:pk>/editar/", views.audit_update, name="audit_update"),
    path("app/findings/", views.finding_list, name="finding_list"),
    path("app/findings/nuevo/", views.finding_create, name="finding_create"),
    path("app/findings/<int:pk>/editar/", views.finding_update, name="finding_update"),
    path("admin/", admin.site.urls),
]
