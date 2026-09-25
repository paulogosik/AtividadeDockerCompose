from django import forms

from .models import Arquivo


class ArquivoForm(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields = ["arquivo"]
        labels = {"arquivo": "Selecione um arquivo"}

    def clean_arquivo(self):
        arquivo = self.cleaned_data["arquivo"]
        if arquivo.size > 10 * 1024 * 1024:
            raise forms.ValidationError("O arquivo deve ter no máximo 10 MB.")
        return arquivo
