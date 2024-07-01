from django.shortcuts import render, redirect, get_object_or_404
from api.models import requisicion

def buscar_view(request):
    if request.method == 'POST':
        id = request.POST['id']

        
        try:
            objeto = requisicion.objects.get(codigo=id)
            context = {
                'requisicion': objeto
            }
            return redirect('editar', id=objeto.id)
        except requisicion.DoesNotExist:
            return render(request, 'Requisicion.html', {'error': 'ID no encontrado'})
    return render(request, 'Requisicion.html')

