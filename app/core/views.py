from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ActivoForm, AuditoriaForm, FindingForm
from .models import Activo, Auditoria, AuditoriaActivo, Finding


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
    audits = Auditoria.objects.prefetch_related("auditoria_activos__activo").all()
    return render(request, "core/audit_list.html", {"audits": audits})


@login_required
def audit_create(request):
    if request.method == "POST":
        form = AuditoriaForm(request.POST)
        if form.is_valid():
            audit = form.save(commit=False)
            audit.creado_por = request.user
            audit.save()
            form.save_activos(audit)
            messages.success(request, "Auditoría creada con activos autorizados.")
            return redirect("audit_list")
    else:
        form = AuditoriaForm()

    return render(request, "core/audit_form.html", {
        "form": form,
        "title": "Nueva auditoría",
        "submit_label": "Crear auditoría",
    })


@login_required
def audit_update(request, pk):
    audit = get_object_or_404(Auditoria, pk=pk)

    if request.method == "POST":
        form = AuditoriaForm(request.POST, instance=audit)
        if form.is_valid():
            audit = form.save()
            form.save_activos(audit)
            messages.success(request, "Auditoría actualizada.")
            return redirect("audit_list")
    else:
        form = AuditoriaForm(instance=audit)

    return render(request, "core/audit_form.html", {
        "form": form,
        "audit": audit,
        "title": "Editar auditoría",
        "submit_label": "Guardar auditoría",
    })



@login_required
def audit_detail(request, pk):
    audit = get_object_or_404(
        Auditoria.objects.select_related("creado_por").prefetch_related(
            "auditoria_activos__activo",
            "findings__activo",
        ),
        pk=pk,
    )
    asset_links = audit.auditoria_activos.select_related("activo").order_by("activo__nombre")
    findings = audit.findings.select_related("activo").order_by("-creado_en", "titulo")
    return render(request, "core/audit_detail.html", {
        "audit": audit,
        "asset_links": asset_links,
        "findings": findings,
    })

@login_required
def finding_list(request):
    findings = Finding.objects.select_related("auditoria", "activo").all()
    return render(request, "core/finding_list.html", {"findings": findings})


@login_required
def finding_audit_assets(request, pk):
    audit = get_object_or_404(Auditoria, pk=pk)
    assets = Activo.objects.filter(
        auditoria_activos__auditoria=audit,
        activo=True,
        autorizado=True,
    ).distinct().order_by("nombre")

    return JsonResponse({
        "assets": [
            {"id": asset.pk, "label": str(asset)}
            for asset in assets
        ]
    })


@login_required
def finding_create(request):
    if request.method == "POST":
        form = FindingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Finding manual creado.")
            return redirect("finding_list")
    else:
        form = FindingForm()

    return render(request, "core/finding_form.html", {
        "form": form,
        "title": "Nuevo finding",
        "submit_label": "Crear finding",
    })



@login_required
def finding_detail(request, pk):
    finding = get_object_or_404(
        Finding.objects.select_related("auditoria", "activo"),
        pk=pk,
    )
    return render(request, "core/finding_detail.html", {"finding": finding})

@login_required
def finding_update(request, pk):
    finding = get_object_or_404(Finding, pk=pk)

    if request.method == "POST":
        form = FindingForm(request.POST, instance=finding)
        if form.is_valid():
            form.save()
            messages.success(request, "Finding actualizado.")
            return redirect("finding_list")
    else:
        form = FindingForm(instance=finding)

    return render(request, "core/finding_form.html", {
        "form": form,
        "finding": finding,
        "title": "Editar finding",
        "submit_label": "Guardar finding",
    })
