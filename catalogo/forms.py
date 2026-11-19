from django import forms

from .models import Livro


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        # Apenas estes campos podem ser preenchidos pelo formulário.
        fields = ["nome", "autor", "descricao", "categoria"]
