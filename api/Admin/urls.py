from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .Utensilios.views import Utensilios
urlpatterns = [
    path('admin/agregar_utensilios/', Utensilios.as_view(), name='utensilios'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)