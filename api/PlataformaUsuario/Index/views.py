from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors
from datetime import datetime
from api.models import requisicion
from django.contrib import messages
import io
from django.core.files.base import ContentFile
from .codigo import generar_codigo_unico
from api.models import utensilios
from django.core.paginator import Paginator
from django.urls import reverse
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
from django.core.files.base import ContentFile
from django.core.mail import send_mail  # Importa send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from api.models import requisicion, utensilios
import io

class Index(APIView):
    template_name = "index.html"

    def get(self, request):
        utensilios_list = utensilios.objects.all()
        search_query = request.GET.get('search', '')
        
        if search_query:
            utensilios_list = utensilios.objects.filter(nombre__icontains=search_query)
        
        paginator = Paginator(utensilios_list, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {
            'page_obj': page_obj,
            'search_query': search_query 
        })
    
    def post(self, request):
        try:
            user = request.user
            grupo = request.POST.get('grupo')
            inicio = request.POST.get('inicio')
            fecha = request.POST.get('fecha')
            fin = request.POST.get('fin')
            docente = request.POST.get('docente')
            asignatura = request.POST.get('asignatura')
            taller = request.POST.get('taller')

            utensilios_list = []
            for key, value in request.POST.items():
                if key.startswith('utensilios'):
                    parts = key.split('[')
                    index = int(parts[1][:-1])
                    field = parts[2][:-1]

                    while len(utensilios_list) <= index:
                        utensilios_list.append({})

                    utensilios_list[index][field] = value

            utensilios_finales = []
            for u in utensilios_list:
                if 'nombre' in u and 'cantidad' in u:
                    utensilio_id = u.get('id', '')
                    utensilio = utensilios.objects.get(id=utensilio_id)
                    print(utensilio_id)
                    utensilio.incrementar_solicitud()
                    utensilios_finales.append({
                        'id': utensilio.id,
                        'nombre': utensilio.nombre,
                        'cantidad_maxima': utensilio.cantidad,
                        'cantidad': u['cantidad']
                    })

            # Generación del PDF (sigue igual)
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

            # Preparar el correo
            subject = 'Requisición de Utensilios'
            html_message = render_to_string('requisicion_email.html', {'user': user})
            plain_message = 'Adjunto encontrarás el PDF de la requisición de utensilios que solicitaste.'  # Mensaje de texto plano
            from_email = settings.EMAIL_HOST_USER
            to_email = [user.email]

            # Crear el EmailMessage para enviar el correo con el PDF adjunto
            email = EmailMessage(
                subject,
                plain_message,
                from_email,
                to_email,
            )
            email.attach(f'Requisicion_{fecha}.pdf', pdf_content, 'application/pdf')
            email.html_message = html_message  # Establece el mensaje HTML

            # Enviar el correo
            email.send(fail_silently=False)

            # Guarda el PDF en el modelo si es necesario
            temp_file = ContentFile(pdf_content)
            temp_file_name = f"Requisicion_{fecha}.pdf"
            codigo_unico = generar_codigo_unico()

            oficio = requisicion.objects.create(
                codigo=codigo_unico,
                hora_inicio=inicio,
                hora_fin=fin,
                grupo=grupo,
                pdf=temp_file,
                created_date=fecha,
                docente=docente,
                items=utensilios_finales,
            )
            oficio.users.add(user)
            oficio.pdf.save(temp_file_name, temp_file)
            messages.success(request, 'La requisición se generó correctamente y se ha enviado el correo.')
            return JsonResponse({'success': True, 'redirect_url': reverse('index')})

        except Exception as e:
            print(f'Error al generar el PDF: {str(e)}')
            messages.error(request, f'Error al generar el PDF: {str(e)}')
            return render(request, '404.html')

            