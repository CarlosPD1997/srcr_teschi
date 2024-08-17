from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.contrib import messages
from api.models import Users, Semester  # Asegúrate de importar tu modelo de usuarios y semestres

class SignUp(APIView):
    template_name = "register.html"

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
        matricula = request.POST['matricula']

        # Verifica si el usuario ya existe
        if Users.objects.filter(email=email).exists():
            messages.warning(request, 'Error. Este correo ya está registrado.')
            return render(request, 'register.html')
        
        if Users.objects.filter(matricula=matricula).exists():
            messages.warning(request, 'Error. Esta matrocula ya está registrada.')
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
                username=email,
                matricula=matricula
            )
            user.set_password(password)
            user.full_clean()  
            user.save()
           

            # Configuración del correo electrónico
            subject = 'Bienvenido!'
            html_message = render_to_string('registration_email.html', 
                                            {'user': user,
                                             'password': password})
            plain_message = strip_tags(html_message)  # Elimina etiquetas HTML para clientes de correo que no admiten HTML
            from_email = settings.EMAIL_HOST_USER
            to_email = [email]

            # Envío del correo
            send_mail(
                subject,
                plain_message,
                from_email,
                to_email,
                html_message=html_message,
                fail_silently=False  # Cambia esto a True si no quieres que se lance una excepción al fallar el envío
            )

            # Mensaje de éxito
            messages.success(request, 'Registro exitoso. Revisa tu correo para más detalles.')
            return render(request, 'register.html')

        except Exception as e:
            print("Fallo", e)
            messages.error(request, f'Error al registrar la cuenta')
            return render(request, 'register.html')
