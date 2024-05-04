from django import forms
from django.core.exceptions import ValidationError


class AgendaForm(forms.Form):
    nome = forms.CharField(max_length=150)
    telefone = forms.CharField(max_length=20)
        
    def clean_nome(self):
        nome = self.cleaned_data['nome']
        return nome.upper()

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        if telefone.startswith('19'):
            return telefone
        raise ValidationError('DDD válido somente o 19')
