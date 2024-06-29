from rest_framework.views import APIView
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors
from datetime import datetime
from django.contrib.staticfiles import finders
from reportlab.lib.units import inch
from reportlab.platypus import Frame
from api.models import requisicion
from django.contrib import messages
import io
import uuid
from django.core.files.base import ContentFile
import base64
from api.models import utensilios
from django.core.paginator import Paginator
from django.template.loader import render_to_string


# Create your views here.
def generar_codigo_unico():
        random_uuid = uuid.uuid4()
    
        # Convertir el UUID a bytes
        uuid_bytes = random_uuid.bytes
        
        # Codificar en Base64 y obtener una cadena
        base64_uuid = base64.urlsafe_b64encode(uuid_bytes).decode('utf-8')
        
        # Tomar los primeros 8 caracteres
        codigo_corto = base64_uuid[:8]
        
        return codigo_corto

class Index(APIView):
    template_name="index.html"
    def get(self, request):
        usuario = request.user
        utensilios_list = utensilios.objects.all()
        search_query = request.GET.get('search', '')  # Obtén el término de búsqueda del parámetro GET
        
        # Filtra los utensilios basados en el término de búsqueda si existe
        if search_query:
            utensilios_list = utensilios.objects.filter(nombre__icontains=search_query)
        else:
            utensilios_list = utensilios.objects.all()  # Obtén todos los utensilios si no hay término de búsqueda

        paginator = Paginator(utensilios_list, 12)  # Mostrar 10 utensilios por página
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
                                                        'search_query': search_query 
        })
    
    
    
    def post(self,request):
        try:
            user = request.user
            grupo = request.POST.get('grupo')
            inicio = request.POST.get('inicio')
            fecha = request.POST.get('fecha')
            fin = request.POST.get('fin')
            docente = request.POST.get('docente')
            asignatura = request.POST.get('asignatura')
            taller = request.POST.get('taller')

            utensilios = []
            for key, value in request.POST.items():
                if key.startswith('utensilios'):
                    parts = key.split('[')
                    index = int(parts[1][:-1])
                    field = parts[2][:-1]
                    while len(utensilios) <= index:
                        utensilios.append({})
                    utensilios[index][field] = value
            utensilios = [[u['nombre'], u['cantidad']] for u in utensilios if 'nombre' in u and 'cantidad' in u]
            print(utensilios)
            fecha_actual = datetime.now().strftime('%Y-%m-%d')

            # Crear el PDF en memoria
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
            elements = []

            # Título y datos del encabezado
            title = "2024. Año del Bicentenario de la Erección del Estado Libre y Soberano de México"
            header_data = [
                ["PRÁCTICAS DE LOS TALLERES DE LA LICENCIATURA EN GASTRONOMÍA "],
                ["FECHA:", fecha_actual, "GRUPO:", grupo],
                ["HORA DE INICIO:", inicio, "HORA DE TÉRMINO:", fin],
                ["DOCENTE:", docente, "ASIGNATURA:", asignatura],
                ["TALLER:", taller, "", ""]
            ]

            header_table = Table(header_data, colWidths=[150, 200, 150, 200])
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

            # Agregar la tabla de utensilios
            utensilios_data = [
                ["NOMBRE \n DE \n UTENSILIOS", "CANTIDAD \n REQUERIDA \n  POR EL \n ESTUDIANTE", "CANTIDAD \n ENTREGADA \n POR EL ALMACÉN", "CANTIDAD \n RECIBIDA \n POR \n ENCARGADO \n DEL \n ALMACÉN Y \n ENCARGADO \n DE ÁREA"],
            ]
            for utensilio in utensilios:
                utensilios_data.append([utensilio[0], utensilio[1], "", ""])

            utensilios_table = Table(utensilios_data, colWidths=[150, 100, 100, 100])
            utensilios_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(utensilios_table)

            # Añadir la tabla de firma
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

            # Guardar el PDF en un archivo temporal
            temp_file = ContentFile(pdf_content)
            temp_file_name = f"Requisicion_{fecha_actual}.pdf"
            codigo_unico = generar_codigo_unico()  # Asegúrate de que esta función está definida

            # Crear el objeto Requisicion y guardar el PDF en el campo FileField
            oficio = requisicion.objects.create(
                codigo=codigo_unico,
                hora_inicio=inicio,
                hora_fin=fin,
                grupo=grupo,
                pdf=temp_file,
                created_date=fecha_actual,
                docente=docente
            )
            oficio.users.add(user)
            # Guardar el archivo en el FileField
            oficio.pdf.save(temp_file_name, temp_file)

            # Retornar el archivo PDF como respuesta
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename={temp_file_name}'
            return response

        except Exception as e:
            print(f'Error al generar el PDF: {str(e)}')
            messages.error(request, f'Error al generar el PDF: {str(e)}')
            return render(request, '404.html')
    