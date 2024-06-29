from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
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
        username = request.POST['username']
        password = request.POST['password']
        print(f"Autenticando usuario: {username} con contraseña: {password}")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print(f"Usuario autenticado: {user}")
            auth_login(request, user)
            return redirect('index')
        else:
            print("Autenticación fallida")
            messages.error(request, 'Usuario no encontrado')
            return render(request, 'login.html', {'form': AuthenticationForm()})
