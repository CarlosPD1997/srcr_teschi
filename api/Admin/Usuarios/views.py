from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from api.models import Users
# Create your views here.
from django.core.paginator import Paginator

class UsersApi(APIView):
    template_name="UsuariosHis.html"
    
    # Obtener todas las requisiciones del usuario
    def get(self, request):
        user = request.user
        if user.is_superuser:
            usuarios = Users.objects.all()

            # Filtrar usuarios que son superusuarios
            super_usuarios = Users.objects.filter(is_superuser=True)

            # Filtrar usuarios que no son superusuarios
            no_super_usuarios = Users.objects.filter(is_superuser=False)
            paginator = Paginator(usuarios, 12)  
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {
            'usuarios': usuarios,
                'super_usuarios': super_usuarios,
                'no_super_usuarios': no_super_usuarios,
                'page_obj': page_obj

            }

            return render(request, self.template_name, context)
        else:
            return render(request, '404.html', {
                'status_code': 403,
                'error_message': 'Parece que ha ocurrido un error.'
            }, status=403)
    