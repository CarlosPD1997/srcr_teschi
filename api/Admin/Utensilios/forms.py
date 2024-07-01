from django import forms
from api.models import utensilios

class UtensilioForm(forms.ModelForm):
    class Meta:
        model = utensilios
        fields = ['nombre', 'descripcion', 'cantidad', 'tamaño', 'img']
