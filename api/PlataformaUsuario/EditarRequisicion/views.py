from django.shortcuts import render, get_object_or_404, redirect
from api.models import requisicion
from .forms import editar_requisicion

def editar_view(request, id):
    objeto = get_object_or_404(requisicion, id=id)
    context = {
        'requisicion': objeto
    }
    return render(request, 'editar_requisicion.html', context)
