from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from api.models import utensilios

@csrf_exempt
@require_http_methods(["POST"])
def eliminar_utensilio(request, utensilio_id):
    try:
        utensilio = get_object_or_404(utensilios, id=utensilio_id)
        utensilio.delete()
        messages.success(request, "Utensilio eliminado correctamente.")  # Mensaje de éxito
    except Exception as e:
        messages.error(request, "Error al eliminar el utensilio. Por favor, inténtalo de nuevo.")  # Mensaje de error

    return redirect('utensilios')  # Redirige a la lista de utensilios
