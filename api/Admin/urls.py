from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .Utensilios.views import Utensilios
from .Utensilios.Edit.views import EditarUtensilioView
from .Utensilios.Delete.views import eliminar_utensilio

urlpatterns = [
    path('admin/agregar_utensilios/', Utensilios.as_view(), name='utensilios'),
    path('utensilios/editar/<int:utensilio_id>/', EditarUtensilioView.as_view(), name='editar_utensilio'),
    path('utensilios/eliminar/<int:utensilio_id>/', eliminar_utensilio, name='eliminar_utensilio'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)