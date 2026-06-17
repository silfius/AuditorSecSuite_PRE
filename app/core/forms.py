from django import forms

from .models import Activo, Auditoria, AuditoriaActivo, Finding
from .models import CheckDefinition, AuditCheckPlan
from django.core.exceptions import ValidationError


class ActivoForm(forms.ModelForm):
    class Meta:
        model = Activo
        fields = ["nombre", "tipo", "valor", "entorno", "autorizado", "activo", "notas"]
        widgets = {
            "notas": forms.Textarea(attrs={"rows": 4}),
        }
        help_texts = {
            "autorizado": "Marca este campo solo si el activo es propio o existe autorización explícita para auditarlo.",
            "valor": "Host, IP, URL, dominio, servicio o identificador controlado.",
        }

    def clean_nombre(self):
        return self.cleaned_data["nombre"].strip()

    def clean_valor(self):
        return self.cleaned_data["valor"].strip()

    def clean_entorno(self):
        return self.cleaned_data.get("entorno", "").strip()

class AuditoriaForm(forms.ModelForm):
    activos = forms.ModelMultipleChoiceField(
        queryset=Activo.objects.none(),
        required=True,
        widget=forms.CheckboxSelectMultiple,
        help_text="Selecciona únicamente activos autorizados y activos.",
    )

    class Meta:
        model = Auditoria
        fields = ["nombre", "alcance", "perfil", "estado", "activos"]
        widgets = {
            "alcance": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        auditables = Activo.objects.filter(activo=True, autorizado=True).order_by("nombre")
        self.fields["activos"].queryset = auditables
        if self.instance and self.instance.pk and not self.is_bound:
            self.fields["activos"].initial = self.instance.auditoria_activos.values_list("activo_id", flat=True)

    def clean_nombre(self):
        return self.cleaned_data["nombre"].strip()

    def clean_alcance(self):
        return self.cleaned_data["alcance"].strip()

    def clean_activos(self):
        activos = self.cleaned_data["activos"]
        invalidos = [activo for activo in activos if not activo.puede_auditarse()]
        if invalidos:
            raise forms.ValidationError("Solo se pueden vincular activos activos y autorizados.")
        return activos

    def save_activos(self, auditoria):
        AuditoriaActivo.objects.filter(auditoria=auditoria).delete()
        AuditoriaActivo.objects.bulk_create([
            AuditoriaActivo(auditoria=auditoria, activo=activo)
            for activo in self.cleaned_data["activos"]
        ])

_FINDING_MODEL_FIELD_NAMES = {field.name for field in Finding._meta.fields}
_FINDING_FORM_FIELDS = [
    name for name in [
        "auditoria",
        "activo",
        "titulo",
        "descripcion",
        "recomendacion",
        "severidad",
        "estado",
        "herramienta",
    ]
    if name in _FINDING_MODEL_FIELD_NAMES
]


class FindingForm(forms.ModelForm):
    class Meta:
        model = Finding
        fields = _FINDING_FORM_FIELDS
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 5}),
            "recomendacion": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        auditoria = None
        auditoria_id = None

        if self.is_bound:
            auditoria_id = self.data.get(self.add_prefix("auditoria")) or self.data.get("auditoria")
        elif self.instance and self.instance.pk:
            auditoria = self.instance.auditoria
            auditoria_id = auditoria.pk

        if auditoria is None and auditoria_id:
            try:
                auditoria = Auditoria.objects.get(pk=auditoria_id)
            except (Auditoria.DoesNotExist, ValueError, TypeError):
                auditoria = None

        if "auditoria" in self.fields:
            self.fields["auditoria"].queryset = Auditoria.objects.order_by("-creado_en", "nombre")

        if "activo" in self.fields:
            if auditoria is not None:
                self.fields["activo"].queryset = Activo.objects.filter(
                    auditoria_activos__auditoria=auditoria,
                    activo=True,
                    autorizado=True,
                ).distinct().order_by("nombre")
            else:
                self.fields["activo"].queryset = Activo.objects.none()

    def clean_titulo(self):
        return self.cleaned_data["titulo"].strip()

    def clean_herramienta(self):
        return self.cleaned_data.get("herramienta", "").strip()

    def clean(self):
        cleaned = super().clean()
        auditoria = cleaned.get("auditoria")
        activo = cleaned.get("activo")

        if auditoria and activo:
            vinculado = AuditoriaActivo.objects.filter(auditoria=auditoria, activo=activo).exists()
            if not vinculado:
                self.add_error("activo", "El activo seleccionado no pertenece a la auditoría.")
            elif not activo.puede_auditarse():
                self.add_error("activo", "El activo seleccionado no es auditable.")

        return cleaned



class CheckDefinitionForm(forms.ModelForm):
    class Meta:
        model = CheckDefinition
        fields = [
            "codigo",
            "nombre",
            "descripcion",
            "categoria",
            "engine_key",
            "tipo_activo_aplicable",
            "is_enabled",
            "nivel_riesgo_operativo",
            "requiere_autorizacion",
        ]


class AuditCheckPlanForm(forms.ModelForm):
    class Meta:
        model = AuditCheckPlan
        fields = ["check_definition", "activo", "estado", "motivo_bloqueo"]

    def __init__(self, *args, auditoria=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.auditoria = auditoria

        self.fields["check_definition"].queryset = (
            CheckDefinition.objects
            .filter(is_enabled=True)
            .exclude(nivel_riesgo_operativo=CheckDefinition.RISK_INTRUSIVE)
            .order_by("categoria", "codigo")
        )

        if auditoria is None:
            self.fields["activo"].queryset = Activo.objects.none()
        else:
            activos_ids = [
                relacion.activo_id
                for relacion in AuditoriaActivo.objects.select_related("activo").filter(auditoria=auditoria)
                if relacion.activo and relacion.activo.puede_auditarse()
            ]
            self.fields["activo"].queryset = Activo.objects.filter(pk__in=activos_ids).order_by("nombre")

        selected_asset = self._selected_asset_for_check_filter()
        if selected_asset is not None:
            applicable_ids = [
                check.pk
                for check in self.fields["check_definition"].queryset
                if check.applies_to_asset(selected_asset)
            ]
            self.fields["check_definition"].queryset = self.fields["check_definition"].queryset.filter(
                pk__in=applicable_ids
            )

        self.fields["check_definition"].help_text = (
            "Solo se muestran checks activos, no intrusivos y aplicables al tipo de activo seleccionado."
        )

    def _selected_asset_for_check_filter(self):
        asset_id = None

        if self.is_bound:
            asset_id = self.data.get(self.add_prefix("activo"))
        elif getattr(self.instance, "activo_id", None):
            asset_id = self.instance.activo_id

        if not asset_id:
            return None

        try:
            return self.fields["activo"].queryset.get(pk=asset_id)
        except (Activo.DoesNotExist, ValueError, TypeError):
            return None

    def clean(self):
        cleaned_data = super().clean()
        if self.auditoria is not None and cleaned_data.get("activo") and cleaned_data.get("check_definition"):
            plan = AuditCheckPlan(
                auditoria=self.auditoria,
                activo=cleaned_data.get("activo"),
                check_definition=cleaned_data.get("check_definition"),
                estado=cleaned_data.get("estado") or AuditCheckPlan.STATE_PLANNED,
                motivo_bloqueo=cleaned_data.get("motivo_bloqueo") or "",
            )
            try:
                plan.clean()
            except ValidationError as exc:
                raise forms.ValidationError(exc)
        return cleaned_data
