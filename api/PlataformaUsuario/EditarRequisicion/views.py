from django.shortcuts import render, get_object_or_404
from api.models import requisicion, utensilios as uten
from django.core.paginator import Paginator
import json

def editar_view(request, id):
    objeto = get_object_or_404(requisicion, id=id)

    utensilios = objeto.items

    search_query = request.GET.get('search', '')  # Obtén el término de búsqueda del parámetro GET
    
    if search_query:
        utensilios_list = uten.objects.filter(nombre__icontains=search_query)
    else:
        utensilios_list = uten.objects.all()

    paginator = Paginator(utensilios_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'requisicion': objeto,
        'utensilios': utensilios,  # Pasa la lista de utensilios directamente al contexto
        'page_obj': page_obj,
        'search_query': search_query 
    }
    return render(request, 'editar_requisicion.html', context)
