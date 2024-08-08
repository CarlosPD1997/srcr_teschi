from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib import messages
from django.http import JsonResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
import io
import json
from .codigo import generar_codigo_unico
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors
from datetime import datetime
from django.contrib import messages
import io
from django.core.files.base import ContentFile
from .codigo import generar_codigo_unico
from api.models import utensilios
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import  HttpResponseRedirect
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage  # Importa EmailMessage para enviar correos
from django.contrib import messages
from api.models import requisicion, utensilios
import io
from django.conf import settings
from django.http import JsonResponse

from rest_framework.views import APIView
from django.shortcuts import render

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors

from django.template.loader import render_to_string
from django.contrib import messages

import io

class EditarRequisicionView(APIView):
    template_name = 'editar_requisicion.html'

    def get(self, request, id):
        requisicion_obj = get_object_or_404(requisicion, id=id)
        
        utensilios_list = utensilios.objects.all()
        search_query = request.GET.get('search', '')
        
        if search_query:
            utensilios_list = utensilios.objects.filter(nombre__icontains=search_query)
        
        paginator = Paginator(utensilios_list, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'requisicion': requisicion_obj,
            'utensilios': requisicion_obj.items,
            'page_obj': page_obj,
            'search_query': search_query 
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        objeto = get_object_or_404(requisicion, id=id)
        try:
            # Obtén los datos del formulario
            grupo = request.POST.get('grupo')
            inicio = request.POST.get('inicio')
            fecha = request.POST.get('fecha')
            fin = request.POST.get('fin')
            docente = request.POST.get('docente')
            asignatura = request.POST.get('asignatura')
            taller = request.POST.get('taller')

            # Procesa los utensilios del formulario
            utensilios = []
            for key, value in request.POST.items():
                if key.startswith('utensilios'):
                    parts = key.split('[')
                    index = int(parts[1][:-1])
                    field = parts[2][:-1]

                    while len(utensilios) <= index:
                        utensilios.append({})

                    utensilios[index][field] = value

            utensilios_finales = [
                {
                    'id': u.get('id', ''),
                    'nombre': u.get('nombre', ''),
                    'cantidad_maxima': u.get('cantidad_maxima', ''),
                    'cantidad': u.get('cantidad', '')
                }
                for u in utensilios if 'nombre' in u and 'cantidad' in u
            ]

            # Actualiza los utensilios en el modelo de requisición
            objeto.hora_inicio = inicio
            objeto.hora_fin = fin
            objeto.grupo = grupo
            objeto.docente = docente
            objeto.items = utensilios_finales  # Suponiendo que 'items' es un campo JSON o similar
            objeto.save()

            # Genera el nuevo PDF
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []

            header_data = [
                ["PRÁCTICAS DE LOS TALLERES DE LA LICENCIATURA EN GASTRONOMÍA"],
                ["FECHA:", fecha, "GRUPO:", grupo],
                ["HORA DE INICIO:", inicio, "HORA DE TÉRMINO:", fin],
                ["DOCENTE:", docente, "ASIGNATURA:", asignatura],
                ["TALLER:", taller, "", ""]
            ]

            header_table = Table(header_data, colWidths=[150, 150, 150, 150])
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('SPAN', (0, 0), (-1, 0)),
                ('BACKGROUND', (0, 0), (0, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (0, 0), colors.whitesmoke),
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 1), (-1, -1), 1, colors.black),
            ]))
            elements.append(header_table)
            elements.append(Spacer(1, 20))

            utensilios_data = [
                ["NOMBRE \n DE \n UTENSILIOS", 
                 "CANTIDAD \n REQUERIDA \n  POR EL \n ESTUDIANTE", 
                 "CANTIDAD \n ENTREGADA \n POR EL ALMACÉN", 
                 "CANTIDAD \n RECIBIDA \n POR \n ENCARGADO \n DEL \n ALMACÉN Y \n ENCARGADO \n DE ÁREA"],
            ]
            for utensilio in utensilios_finales:
                utensilios_data.append([utensilio['nombre'], utensilio['cantidad'], "", ""])

            utensilios_table = Table(utensilios_data, colWidths=[150, 100, 100, 100])
            utensilios_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(utensilios_table)

            firma_data = [
                ["__________________ \n FIRMA DE ALMACÉN"]
            ]
            firma_table = Table(firma_data, colWidths=[200], rowHeights=[60])
            firma_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(Spacer(0, 20))
            elements.append(firma_table)

            doc.build(elements)

            buffer.seek(0)
            pdf_content = buffer.getvalue()

            # Preparar y enviar el correo
            subject = 'Requisición de Utensilios Actualizada'
            html_message = render_to_string('requisicion_email.html', {'user': request.user})
            plain_message = 'Adjunto encontrarás el PDF de la requisición de utensilios que solicitaste.'  # Mensaje de texto plano
            from_email = settings.EMAIL_HOST_USER
            to_email = ['almacenteschi2024@gmail.com']

            email = EmailMessage(
                subject,
                plain_message,
                from_email,
                to_email,
            )
            email.attach(f'Requisicion_{fecha}.pdf', pdf_content, 'application/pdf')
            email.html_message = html_message

            email.send(fail_silently=False)

            # Actualizar el PDF en el modelo
            temp_file = ContentFile(pdf_content)
            temp_file_name = f"Requisicion_{fecha}.pdf"
            objeto.pdf.save(temp_file_name, temp_file)

            messages.success(request, 'La requisición se actualizó correctamente y se ha enviado el correo.')
            return redirect(reverse('index'))

        except Exception as e:
            print(f'Error al actualizar la requisición: {str(e)}')
            messages.error(request, f'Error al actualizar la requisición: {str(e)}')
            return render(request, '404.html')