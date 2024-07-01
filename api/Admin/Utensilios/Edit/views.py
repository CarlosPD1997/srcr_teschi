from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from api.models import utensilios
from django import forms
from django.shortcuts import render

class UtensilioForm(forms.ModelForm):
    img = forms.ImageField(label="Utensilio", required=False ,widget=forms.FileInput(attrs={'class': 'user'}))
    class Meta:
        model = utensilios
        fields = ['nombre', 'descripcion', 'cantidad', 'tamaño', 'img']

class EditarUtensilioView(View):
    def get(self, request, utensilio_id):
        utensilio = get_object_or_404(utensilios, id=utensilio_id)
        form = UtensilioForm(instance=utensilio)
        return render(request, 'editar_utensilios.html', {'form': form, 'utensilio': utensilio})

    def post(self, request, utensilio_id):
        utensilio = get_object_or_404(utensilios, id=utensilio_id)
        form = UtensilioForm(request.POST, request.FILES, instance=utensilio)
        if form.is_valid():
            utensilio = form.save(commit=False)

            # Verificar si 'img' está en request.FILES, si no, mantener la imagen existente
            if 'img' in request.FILES:
                utensilio.imagen = request.FILES['img']

            utensilio.save()
            return redirect('utensilios')
        else:
            return render(request, '404.html')
        
        
    def delete(self, request, utensilio_id):
        try:
            utensilio = get_object_or_404(utensilios, id=utensilio_id)
            utensilio.delete()
            return JsonResponse({'success': True, 'message': 'Utensilio eliminado correctamente.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})