from rest_framework.views import APIView
from django.shortcuts import render, redirect
from api.models import utensilios
from django.http import JsonResponse
from django import forms
from django.core.paginator import Paginator
from django.contrib import messages

class UtensilioForm(forms.ModelForm):
    img = forms.ImageField(label="Utensilio", required=False ,widget=forms.FileInput(attrs={'class': 'user'}))
    class Meta:
        model = utensilios
        fields = ['nombre', 'descripcion', 'cantidad', 'tamaño', 'img']
    

class Utensilios(APIView):
    template_name="utensilios.html"
    def get(self, request):
        usuario = request.user
        if usuario.is_superuser:
            utensilios_list = utensilios.objects.all()
            search_query = request.GET.get('search', '')  # Obtén el término de búsqueda del parámetro GET
            
            # Filtra los utensilios basados en el término de búsqueda si existe
            if search_query:
                utensilios_list = utensilios.objects.filter(nombre__icontains=search_query)
            else:
                utensilios_list = utensilios.objects.all()  # Obtén todos los utensilios si no hay término de búsqueda

            paginator = Paginator(utensilios_list, 12)  # Mostrar 10 utensilios por página
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            usuario_data = {
                    'username': usuario.username,
                    'email': usuario.email,
                    'photo': usuario.profile_photo,
                    'name': usuario.first_name
                    # Agrega otros campos que quieras incluir
                }
            
            return render(request, self.template_name,  {'usuario': usuario_data, 
                                                         'page_obj': page_obj, 
                                                         'utensilios_list': utensilios_list})
        else:
            return render(request, '404.html', {
                'status_code': 403,
                'error_message': 'Parece que no estas autorizado.'
            }, status=403)
        
    from django.contrib import messages  # Asegúrate de importar messages

    def post(self, request):
        form = UtensilioForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Guardar datos del formulario
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            cantidad = form.cleaned_data['cantidad']
            tamaño = form.cleaned_data['tamaño']
            
            if 'img' in request.FILES:
                imagen = request.FILES['img']
            else:
                imagen = None  # O puedes usar una imagen predeterminada, si lo prefieres

            utensil = utensilios(
                nombre=nombre,
                descripcion=descripcion,
                cantidad=cantidad,
                tamaño=tamaño,
                img=imagen,
            )

            utensil.save()  # Guardar el objeto completo en la base de datos

            messages.success(request, "Utensilio creado correctamente.")  # Mensaje de éxito
            return redirect('utensilios')  # Cambia esto a la vista que desees redirigir

        else:
            messages.error(request, "Parece que hubo un error en el formulario. Por favor, corrige los errores.")  # Mensaje de error
            return redirect('utensilios')
