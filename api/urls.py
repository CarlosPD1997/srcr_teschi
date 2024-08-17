from django.contrib import admin
from django.urls import path
from .PlataformaUsuario.Index.views import Index
from .PlataformaUsuario.Login.views import Login
from .PlataformaUsuario.SignUp.views import SignUp
from .PlataformaUsuario.Requisicion import views
from .PlataformaUsuario.ForgotPass.views import ForgotPass
from .PlataformaUsuario.ForgotPass.Completado.views import PasswordResetCompleteView
from .PlataformaUsuario.ForgotPass.ReestablecerPass.views import PasswordResetConfirmView
from .PlataformaUsuario.InfoUsuario.views import info
from .PlataformaUsuario.History.views import History
from .PlataformaUsuario.Salir.views import LogoutView
from .PlataformaUsuario.Descarga.views import descargar_requisicion
from .PlataformaUsuario.EditarRequisicion.views import EditarRequisicionView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('generar_requisicion/', Index.as_view(), name='index'),
    path('login/', Login.as_view(), name='login'),
    path('registro/', SignUp.as_view(), name='signup'),
    path('buscar_requisicion/', views.buscar_view , name='requisicion'),
    path('editar_requisicion/<int:id>/', EditarRequisicionView.as_view(), name='editar'),
    path('recuperar_contraseña/', ForgotPass.as_view(), name='recuperar_pass'),
    path('historial_de_requisiciones/', History.as_view(), name='history'),
    path('cerrar_sesion/', LogoutView.as_view(), name='salir'),
    path('informacion_usuario/', info.as_view(), name='info'),
    path('descargar_requisicion/<int:id>/', descargar_requisicion, name='descargar_requisicion'),
     # URL para solicitar el restablecimiento de la contraseña
    path('password_reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # URL para mostrar el mensaje de confirmación después de solicitar el restablecimiento
    path('password_reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)