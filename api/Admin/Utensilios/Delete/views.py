from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from api.models import utensilios

@csrf_exempt
@require_http_methods(["POST"])
def eliminar_utensilio(request, utensilio_id):
    try:
        utensilio = get_object_or_404(utensilios, id=utensilio_id)
        utensilio.delete()
        return redirect('utensilios')  # Redirige a la lista de utensilios
    except Exception as e:
        return redirect('utensilios')  # Puedes redirigir a la misma página con un mensaje de error
