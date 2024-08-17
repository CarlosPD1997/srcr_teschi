from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .Utensilios.views import Utensilios
from .Utensilios.Edit.views import EditarUtensilioView
from .Utensilios.Delete.views import eliminar_utensilio
from .Usuarios.views import UsersApi
from .Usuarios.EditarUsuario.views import EditUser
from .Usuarios.DeleteUser.views import delete_users
from .Usuarios.Agregar.views import AddUser
from .Historial.views import History
from .InfoUsuario.views import info
from .Talleres.views import registrarTalleres
from .Talleres.Eliminar.views import eliminar_taller
from .Talleres.Editar.views import EditarTallerView
from .Dashboard.views import DashboardView

urlpatterns = [
    #Path utensilios
    path('admin/agregar_utensilios/', Utensilios.as_view(), name='utensilios'),
    path('admin/utensilios/editar/<int:utensilio_id>/', EditarUtensilioView.as_view(), name='editar_utensilio'),
    path('admin/utensilios/eliminar/<int:utensilio_id>/', eliminar_utensilio, name='eliminar_utensilio'),
    #path users 
    path('admin/eliminar_usuario/<int:user_id>/', delete_users, name='delete_users'),
    path('admin/editar_usuario/<int:user_id>/', EditUser.as_view(), name='editar_usuario'),
    path('admin/agregar_usuarios/', AddUser.as_view(), name='add_usuarios'),
    path('admin/ver_usuarios', UsersApi.as_view(), name='usuarios'), 
    #History path
    path('admin/historial_requisiciones', History.as_view(), name='HistoryAdmn'), 
    #Info user path
    path('admin/info_usuario', info.as_view(), name='adminfo'), 
    #Talleres y Materias Path
    path('admin/agregar_talleres/', registrarTalleres.as_view(), name='talleres'),
    path('admin/talleres/editar/<int:taller_id>/', EditarTallerView.as_view(), name='editar_taller'),
    path('admin/talleres/eliminar/<int:taller_id>/', eliminar_taller, name='eliminar_taller'),
    # Dashboard view
    path('admin/dashboard/', DashboardView.as_view(), name='dashboard'),


] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)