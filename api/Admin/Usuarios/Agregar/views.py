from django import forms
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views import View
from api.models import Users  # Asegúrate de importar tu modelo de usuario
from django.core.exceptions import ValidationError
from django.contrib import messages

class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = [
            'password',
            'first_name',
            'last_name',
            'username',
            'email',
            'is_staff',
            'is_superuser'
        ]
        widgets = {
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Users.objects.filter(email=email).exists():
            raise ValidationError('Este correo electrónico ya está registrado.')
        return email

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class AddUser(View):

    def get(self, request):
        if request.user.is_superuser:
            form = UserForm()
            return render(request, 'add_usuario.html', {'form': form})
        else:
            return render(request, '404.html', {
                'status_code': 403,
                'error_message': 'Parece que no estás autorizado.'
            }, status=403)

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = 1
            user.save()
            
            messages.success(request, 'El usuario se ha creado exitosamente.')  # Mensaje de éxito
            return redirect('add_usuarios')
        else:
            messages.error(request, 'Error al crear el usuario. Por favor, corrige los errores.')  # Mensaje de error
            return render(request, 'add_usuario.html', {'form': form})
