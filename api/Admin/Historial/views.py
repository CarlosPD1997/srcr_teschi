from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from api.models import requisicion
from django.core.paginator import Paginator

# Create your views here.
class History(APIView):
    template_name="Historial_admin.html"
    
    # Obtener todas las requisiciones del usuario
    def get(self, request):
        user = request.user
        requisiciones = requisicion.objects.all()
        paginator = Paginator(requisiciones, 10)  # 10 elementos por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'page_obj': page_obj
        }
        return render(request, self.template_name, context)
    
    def descargar_requisicion(request, requisicion_id):
        requisiciones = requisicion.objects.get(id=requisicion_id)
        # Aquí iría la lógica para generar y descargar el PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Requisicion_{requisiciones.codigo}.pdf"'
        # ... código para generar el PDF ...
        return response