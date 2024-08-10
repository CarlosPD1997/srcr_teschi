from rest_framework.views import APIView
from django.shortcuts import render, redirect
from api.models import Talleres, Semester
from django.contrib import messages  
from django.core.paginator import Paginator

class registrarTalleres(APIView):

    template_name = "talleres.html"
    
    def get(self, request):
 
        usuario = request.user

        if usuario.is_superuser:
            taller_list = Talleres.objects.all()
            
            semestre = Semester.objects.all()
            search_query = request.GET.get('search', '')  # Obtén el término de búsqueda del parámetro GET
            
            # Filtra los utensilios basados en el término de búsqueda si existe
            if search_query:
                taller_list = Talleres.objects.filter(nombre__icontains=search_query)
            else:
                taller_list = Talleres.objects.all()  # Obtén todos los utensilios si no hay término de búsqueda

            paginator = Paginator(taller_list, 12)  # Mostrar 10 utensilios por página
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
                                                         'talleres_list': taller_list,
                                                         'semestres': semestre
                                                         })
        else:
            return render(request, '404.html', {
                'status_code': 403,
                'error_message': 'Parece que no estas autorizado.'
            }, status=403)
    
    def post(self, request):
        nombre=request.POST['nombre']
        semestre_id = request.POST['semester']

        if not nombre or not semestre_id:
            messages.error(request, "Debes completar el formulario.")
            return render(request, self.template_name)
        
        try:
            semester = Semester.objects.get(id=semestre_id)
            taller = Talleres(
                name=nombre,
                semester=semester
            )
            taller.save()
            messages.success(request, f"El Taller {nombre} ha sido registrado con exito.")
            return render(request, self.template_name)
        
        except Exception as e:
            messages.error(request, f"Ocurrió un error inesperado: {str(e)}")
            return render(request, self.template_name)
