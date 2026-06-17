from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ActivoForm, AuditoriaForm, FindingForm
from .models import Activo, Auditoria, AuditoriaActivo, Finding
from django.urls import NoReverseMatch, reverse
from django.views.decorators.http import require_POST
from .models import CheckDefinition, AuditCheckPlan
from .forms import CheckDefinitionForm, AuditCheckPlanForm


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
    auditoria = get_object_or_404(Auditoria, pk=pk)
    auditoria_activos = AuditoriaActivo.objects.select_related("activo").filter(auditoria=auditoria)
    findings = Finding.objects.select_related("activo").filter(auditoria=auditoria)
    check_plans = AuditCheckPlan.objects.select_related("check_definition", "activo").filter(auditoria=auditoria)

    return render(
        request,
        "core/audit_detail.html",
        {
            "audit": auditoria,
            "auditoria": auditoria,
            "auditoria_activos": auditoria_activos,
            "asset_links": auditoria_activos,
            "audit_assets": auditoria_activos,
            "findings": findings,
            "check_plans": check_plans,
        },
    )

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



def _redirect_to_audit_detail(auditoria):
    for url_name in ("core_audit_detail", "audit_detail"):
        try:
            return redirect(reverse(url_name, args=[auditoria.pk]))
        except NoReverseMatch:
            continue
    return redirect("/app/auditorias/")


@login_required
def check_list(request):
    checks = CheckDefinition.objects.all()
    return render(request, "core/check_list.html", {"checks": checks})


@login_required
def check_create(request):
    if request.method == "POST":
        form = CheckDefinitionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core_check_list")
    else:
        form = CheckDefinitionForm()
    return render(request, "core/check_form.html", {"form": form, "title": "Nuevo check seguro"})


@login_required
def check_update(request, pk):
    check = get_object_or_404(CheckDefinition, pk=pk)
    if request.method == "POST":
        form = CheckDefinitionForm(request.POST, instance=check)
        if form.is_valid():
            form.save()
            return redirect("core_check_list")
    else:
        form = CheckDefinitionForm(instance=check)
    return render(request, "core/check_form.html", {"form": form, "title": "Editar check seguro"})


@login_required
def audit_check_plan_create(request, audit_pk):
    auditoria = get_object_or_404(Auditoria, pk=audit_pk)
    if request.method == "POST":
        form = AuditCheckPlanForm(request.POST, auditoria=auditoria)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.auditoria = auditoria
            plan.creado_por = request.user
            plan.save()
            return _redirect_to_audit_detail(auditoria)
    else:
        form = AuditCheckPlanForm(auditoria=auditoria)

    return render(
        request,
        "core/audit_check_plan_form.html",
        {
            "form": form,
            "auditoria": auditoria,
            "title": "Planificar check seguro",
        },
    )


@login_required
@require_POST
def audit_check_plan_omit(request, audit_pk, plan_pk):
    auditoria = get_object_or_404(Auditoria, pk=audit_pk)
    plan = get_object_or_404(AuditCheckPlan, pk=plan_pk, auditoria=auditoria)
    plan.estado = AuditCheckPlan.STATE_OMITTED
    plan.save()
    return _redirect_to_audit_detail(auditoria)
