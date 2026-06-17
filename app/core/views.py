from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
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
    return render(request, "core/asset_list.html", {"assets": Activo.objects.all()})

@login_required
def audit_list(request):
    return render(request, "core/audit_list.html", {"audits": Auditoria.objects.all()})

@login_required
def finding_list(request):
    return render(request, "core/finding_list.html", {
        "findings": Finding.objects.select_related("auditoria", "activo")
    })
