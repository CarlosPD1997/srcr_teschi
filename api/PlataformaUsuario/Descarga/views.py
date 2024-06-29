from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from api.models import requisicion
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import FileResponse
import os
# Create your views here.
def descargar_requisicion(request, id):
    # Obtener la requisición de la base de datos
    requisiciones = get_object_or_404(requisicion, id=id)

    # Construir la ruta completa al archivo PDF
    pdf_path = os.path.join(settings.MEDIA_ROOT, requisiciones.pdf.name)

    # Crear una respuesta de archivo
    response = FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Requisicion_{requisiciones.codigo}.pdf"'

    return response