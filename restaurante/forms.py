from django import forms
from .models import Prato


class PratoForm(forms.ModelForm):
    class Meta:
        model = Prato
        fields = ['nome', 'categoria', 'descricao', 'preco', 'disponivel']
        labels = {
            'nome': 'Nome',
            'categoria': 'Categoria',
            'descricao': 'Descrição',
            'preco': 'Preço',
            'disponivel': 'Disponível',
        }

    def clean_preco(self):
        preco = self.cleaned_data.get('preco')

        if preco is not None and preco <= 0:
            raise forms.ValidationError('O preço do prato deve ser maior que zero.')

        return preco
