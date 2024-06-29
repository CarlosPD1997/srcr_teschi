import datetime
from api.models import Users, Semester
from django.forms import ValidationError
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from srcr import settings

# Create your views here.
class SignUp(APIView):
    template_name="register.html"
    def get(self, request):
        semestre = Semester.objects.all()
        return render(request, self.template_name, {'semestres': semestre})
    
    def post(self, request):
        name = request.POST['FirstName']
        lastName = request.POST['LastName']
        email = request.POST['mail']
        grupo = request.POST['grupo']
        semester_id = request.POST['semester']
        password = request.POST['PassWord']
        repeat_password = request.POST['RepeatPass']

        # Verifica si el usuario ya existe
        if Users.objects.filter(email=email).exists():
            messages.warning(request, 'Error. Este correo ya está registrado.')
            return render(request, 'register.html')

        if password != repeat_password:
            messages.warning(request, 'Error. Las contraseñas no coinciden.')
            return render(request, 'register.html')

        try:
            semester = Semester.objects.get(id=semester_id)
            user = Users(
                email=email,
                first_name=name,
                last_name=lastName,
                grupo=grupo,
                semester=semester,
                username=email
            )
            user.set_password(password)
            user.full_clean()  
            user.save()
            print("registrado")
            subject = 'Bienvenido a nuestro sitio'
            html_message = render_to_string('registration_email.html', {'user': user})
            plain_message = strip_tags(html_message)  # Eliminar etiquetas HTML para clientes de correo que no admiten HTML
            from_email = settings.EMAIL_HOST_USER
            to_email = [email]
            send_mail(subject, plain_message, from_email, to_email, html_message=html_message)
            return redirect('login')  # Redirige a la página de inicio de sesión
        except Exception as e:
            print("Fallo", e)
            messages.error(request, f'Error al registrar la cuenta: {str(e)}')
            return render(request, 'register.html')
  