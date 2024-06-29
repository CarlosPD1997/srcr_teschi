from django import forms
from api.models import requisicion

class editar_requisicion(forms.ModelForm):
    class Meta:
        model = requisicion
        fields = '__all__'
