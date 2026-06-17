from django import forms

from .models import Activo


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
