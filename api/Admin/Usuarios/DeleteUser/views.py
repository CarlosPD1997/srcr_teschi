from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from api.models import Users
from django.contrib import messages
@csrf_exempt
@require_http_methods(["POST"])
def delete_users(request, user_id):
    try:
        user = get_object_or_404(Users, id=user_id)
        user.delete()
        messages.success(request, f'El usuario  se ha eliminado correctamente.')  # Mensaje de éxito
    except Users.DoesNotExist:
        messages.error(request, 'El usuario no existe.')  # Mensaje de error si el usuario no existe
    except Exception as e:
        messages.error(request, f'Ha ocurrido un error: {str(e)}')  # Mensaje de error genérico
    
    return redirect('usuarios')  # Redirige a la lista de usuarios
