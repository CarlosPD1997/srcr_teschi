from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.conf import settings
from api.models import Users  # Asegúrate de importar tu modelo de usuario
from django.template.loader import render_to_string
from rest_framework.views import APIView
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site

class ForgotPass(APIView):
    template_name = "forgot-password.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = Users.objects.get(email=email)
            
            # Generar un token de restablecimiento de contraseña
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Obtener el dominio actual del sitio
            site = get_current_site(request)
            domain = site.domain

            # Enviar correo electrónico con el enlace para restablecer la contraseña
            subject = 'Recuperación de Contraseña'
            context = {
                'user': user,
                'domain': domain,
                'uid': uid,
                'token': token,
                'protocol': 'https' if request.is_secure() else 'http',
            }
            html_message = render_to_string('recovery_password.html', context)
            plain_message = strip_tags(html_message)

            email = EmailMultiAlternatives(subject, plain_message, settings.EMAIL_HOST_USER, [email])
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=False)

            messages.success(request, 'Se ha enviado un correo con el enlace para restablecer tu contraseña.')
            return redirect('recuperar_pass')  # Redirige a la página de recuperación
        except Users.DoesNotExist:
            messages.error(request, 'No se encontró una cuenta con ese correo electrónico.')
            return render(request, self.template_name)
