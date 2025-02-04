from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from api.models import requisicion, Talleres, utensilios, RequisicionItem
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncMonth

class DashboardView(APIView):
    template_name="dashboard.html"
    
    # Obtener todas las requisiciones del usuario
    def get(self, request):
        user = request.user

        # Talleres que más requisiciones generan
        talleres = Talleres.objects.all()

        # Obtener los talleres con el número de requisiciones que han generado
        talleres_data = []
        for taller in talleres:
            # Contamos las requisiciones de cada taller
            requisiciones_count = requisicion.objects.filter(taller_id=taller.id).count()
            talleres_data.append({'taller': taller.name, 'requisiciones_count': requisiciones_count})
        
        # Ordenamos los talleres por el número de requisiciones generadas
        talleres_data = sorted(talleres_data, key=lambda x: x['requisiciones_count'], reverse=True)

        # Filtrar las requisiciones que contienen "aceite"
        aceite_item_id = 'Aceite'  # Asegúrate de que 'aceite' sea el ID correcto
        aceite_data = []
        
        for taller in talleres:
            # Filtrar requisiciones de este taller
            requisiciones_aceite = requisicion.objects.filter(taller_id=taller.id)
            # Filtrar requisiciones que contienen aceite en los items
            requisiciones_aceite = requisiciones_aceite.filter(
                items__contains=[{'nombre': aceite_item_id}]
            )
            
            # Recolectamos la fecha de las requisiciones y la cantidad de aceite solicitado
            total_aceite = 0  # Total de aceite solicitado en este taller
            for req in requisiciones_aceite:
                # Para cada requisición, buscamos los items relacionados con aceite
                cantidad_aceite = 0
                for item in req.items:
                    if item.get('nombre') == aceite_item_id:
                        cantidad_aceite += int(item.get('cantidad', 0))  # Suponiendo que 'cantidad' está en el item
                if cantidad_aceite > 0:
                    aceite_data.append({'taller': taller.name, 'fecha': req.created_date, 'cantidad_aceite': cantidad_aceite})
                    total_aceite += cantidad_aceite  # Acumulamos el total de aceite

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
            'talleres_data': talleres_data,  # Talleres con más requisiciones
            'aceite_data': aceite_data,  # Datos de aceite solicitado
            'materiales': materiales,
            'requisiciones_mes': requisiciones_mes,
            'requisiciones_ultimos_3_dias': requisiciones_ultimos_3_dias,
        }

        return render(request, self.template_name, context)
