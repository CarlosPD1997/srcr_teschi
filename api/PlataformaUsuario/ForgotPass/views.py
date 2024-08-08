from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.conf import settings
from api.models import Users  # Asegúrate de importar tu modelo de usuario
from django.template.loader import render_to_string
from rest_framework.views import APIView
from django.utils.html import strip_tags

class ForgotPass(APIView):
    template_name = "forgot-password.html"
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = Users.objects.get(email=email)

            # Enviar correo electrónico con los datos de inicio de sesión
            subject = 'Recuperación de Contraseña'
            html_message = render_to_string('recovery_password.html', {
                'user': user,
                'password': user.password  
            })
            plain_message = strip_tags(html_message)

            email = EmailMultiAlternatives(subject, plain_message, settings.EMAIL_HOST_USER, [email])
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=False)

            messages.success(request, 'Se ha enviado un correo con tus datos de inicio de sesión.')
            return redirect('recuperar_pass')  # Redirige a la página de recuperación
        except Users.DoesNotExist:
            messages.error(request, 'No se encontró una cuenta con ese correo electrónico.')
            return render(request, self.template_name)
