from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
class info(APIView):
    template_name="info_usuario.html"
    def get(self, request):
        usuario = request.user
        usuario_data = {
                'username': usuario.username,
                'email': usuario.email,
                'profile_photo': usuario.profile_photo,
                'name': usuario.first_name,
                'grupo': usuario.grupo,
                'semester': usuario.semester,
            }
        
        return render(request, self.template_name,  {'usuario': usuario_data})