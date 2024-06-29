import datetime
from api.models import Users, Semester
from django.forms import ValidationError
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.contrib import messages

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
            messages.success(request, 'Cuenta registrada exitosamente. Por favor, inicia sesión.')

            return redirect('login')  # Redirige a la página de inicio de sesión
        except Exception as e:
            print("Fallo", e)
            messages.error(request, f'Error al registrar la cuenta: {str(e)}')
            return render(request, 'register.html')
  