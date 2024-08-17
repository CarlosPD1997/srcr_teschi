from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from api.models import requisicion, Talleres, utensilios
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

# Create your views here.
class DashboardView(APIView):
    template_name="dashboard.html"
    
    # Obtener todas las requisiciones del usuario
    def get(self, request):
        user = request.user

        # Talleres que más requisiciones generan
        talleres = Talleres.objects.all()
        talleres_data = [
            {'taller': taller.name, 'requisiciones': requisicion.objects.filter(taller=taller).count()}
            for taller in talleres
        ]
        talleres_data = sorted(talleres_data, key=lambda x: x['requisiciones'], reverse=True)

        # Material más solicitado
        materiales = utensilios.objects.all().order_by('-solicitudes')[:6]

        # Requisiciones por mes
        requisiciones_mes = requisicion.objects.annotate(
            month=TruncMonth('created_date')
        ).values('month').annotate(count=Count('id')).order_by('month')

        # Requisiciones de los últimos 3 días
        today = timezone.now().date()
        three_days_ago = today - timedelta(days=3)
        requisiciones_ultimos_3_dias = requisicion.objects.filter(created_date__gte=three_days_ago)

        context = {
            'talleres_data': talleres_data,
            'materiales': materiales,
            'requisiciones_mes': requisiciones_mes,
            'requisiciones_ultimos_3_dias': requisiciones_ultimos_3_dias,
        }



        return render(request, self.template_name, context)
    
    