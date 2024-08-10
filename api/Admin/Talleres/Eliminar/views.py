from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from api.models import Talleres

@csrf_exempt
@require_http_methods(["POST"])
def eliminar_taller(request, taller_id):
    try:
        taller = get_object_or_404(Talleres, id=taller_id)
        taller.delete()
        messages.success(request, "Taller eliminado correctamente.")  # Mensaje de éxito
    except Exception as e:
        messages.error(request, "Error al eliminar el Taller. Por favor, inténtalo de nuevo.")  # Mensaje de error

    return redirect('talleres')  # Redirige a la lista de utensilios
