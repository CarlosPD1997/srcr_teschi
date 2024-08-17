from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class Login(APIView):
    template_name="login.html"
    def get(self, request):
        return render(request, self.template_name,
                                 {'form': AuthenticationForm()})
    
    def post(self, request):
        username = request.POST['username']  # Asumiendo que 'username' es el campo de correo electrónico
        password = request.POST['password']
        # Intentar autenticar al usuario por correo electrónico
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('dashboard')
            else:
                return redirect('index')

        else:
            print("Autenticación fallida")
            messages.error(request, 'Usuario no encontrado o credenciales inválidas')
            return render(request, 'login.html', {'form': AuthenticationForm()})
