from rest_framework.views import APIView
from django.shortcuts import render
from api.models import utensilios
from django.http import JsonResponse
from api.models import utensilios
from django import forms
from django.core.paginator import Paginator

class UtensilioForm(forms.ModelForm):
    img = forms.ImageField(label="Utensilio", required=False ,widget=forms.FileInput(attrs={'class': 'user'}))
    class Meta:
        model = utensilios
        fields = ['nombre', 'descripcion', 'cantidad', 'tamaño', 'img']
    

class Utensilios(APIView):
    template_name="utensilios.html"
    def get(self, request):
        usuario = request.user
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
        
        return render(request, self.template_name,  {'usuario': usuario_data, 'page_obj': page_obj, 'utensilios_list': utensilios_list})
    
    def post(self, request):
        try:
            form = UtensilioForm(request.POST, request.FILES)
            if form.is_valid():
                # Guardar datos del formulario
                nombre = form.cleaned_data['nombre']
                descripcion = form.cleaned_data['descripcion']
                cantidad = form.cleaned_data['cantidad']
                tamaño = form.cleaned_data['tamaño']
                imagen = request.FILES['img']

                utensilio = form.save(commit=False)
                # Guardar la instancia del modelo sin commit para poder añadir la imagen
                utensil = utensilios(
                nombre = nombre,
                descripcion = descripcion,
                cantidad = cantidad,
                tamaño = tamaño,
                img=imagen,
                )

                # Verificar si 'img' está en request.FILES
                
                

                utensil.save()  # Guardar el objeto completo en la base de datos

                message = "Utensilio creado correctamente."
                success = True
            else:
                message = "Error en el formulario. Por favor, revise los datos."
                success = False
        except Exception as e:
            message = str(e)
            success = False

        response_data = {
            'success': success,
            'message': message,
        }

        return JsonResponse(response_data)