from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ActivoForm
from .models import Activo, Auditoria, Finding


def health(request):
    return JsonResponse({"status": "ok", "service": "AuditorSecSuite_PRE"})


@login_required
def dashboard(request):
    return render(request, "core/dashboard.html", {
        "asset_count": Activo.objects.count(),
        "audit_count": Auditoria.objects.count(),
        "finding_count": Finding.objects.count(),
    })


@login_required
def asset_list(request):
    assets = Activo.objects.all()
    return render(request, "core/asset_list.html", {
        "assets": assets,
        "unauthorized_count": assets.filter(autorizado=False).count(),
    })


@login_required
def asset_create(request):
    if request.method == "POST":
        form = ActivoForm(request.POST)
        if form.is_valid():
            asset = form.save()
            if asset.autorizado:
                messages.success(request, "Activo creado y marcado como autorizado.")
            else:
                messages.warning(request, "Activo creado sin autorización. No podrá usarse para auditorías hasta autorizarlo.")
            return redirect("asset_list")
    else:
        form = ActivoForm(initial={"activo": True})

    return render(request, "core/asset_form.html", {
        "form": form,
        "title": "Nuevo activo",
        "submit_label": "Crear activo",
    })


@login_required
def asset_update(request, pk):
    asset = get_object_or_404(Activo, pk=pk)

    if request.method == "POST":
        form = ActivoForm(request.POST, instance=asset)
        if form.is_valid():
            asset = form.save()
            if asset.autorizado:
                messages.success(request, "Activo actualizado y autorizado.")
            else:
                messages.warning(request, "Activo actualizado sin autorización. No podrá usarse para auditorías hasta autorizarlo.")
            return redirect("asset_list")
    else:
        form = ActivoForm(instance=asset)

    return render(request, "core/asset_form.html", {
        "form": form,
        "asset": asset,
        "title": "Editar activo",
        "submit_label": "Guardar activo",
    })


@login_required
def audit_list(request):
    return render(request, "core/audit_list.html", {"audits": Auditoria.objects.all()})


@login_required
def finding_list(request):
    return render(request, "core/finding_list.html", {
        "findings": Finding.objects.select_related("auditoria", "activo")
    })
