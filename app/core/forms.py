from django import forms

from .models import Activo, Auditoria, AuditoriaActivo


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
