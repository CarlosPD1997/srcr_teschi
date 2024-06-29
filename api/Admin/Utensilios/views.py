from rest_framework.views import APIView
from django.shortcuts import render
from api.models import utensilios
from django.http import JsonResponse

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
        
        usuario_data = {
                'username': usuario.username,
                'email': usuario.email,
                'photo': usuario.profile_photo,
                'name': usuario.first_name
                # Agrega otros campos que quieras incluir
            }
        
        return render(request, self.template_name,  {'usuario': usuario_data, 'utensilios_list': utensilios_list})
    
    def post(self, request):
        name = request.POST.get('nombre')
        description = request.POST.get('descripcion')
        quantity = request.POST.get('cantidad')
        size = request.POST.get('tamaño')
        
        try:
            create_utensilio = utensilios.objects.create(
                nombre=name,
                descripcion=description,
                cantidad=quantity,
                tamaño=size
            )
            message = "Utensilio creado correctamente."
            success = True
        except Exception as e:
            message = str(e)
            success = False
        
        response_data = {
            'success': success,
            'message': message,
        }
        
        return JsonResponse(response_data)