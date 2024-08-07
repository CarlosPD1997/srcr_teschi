from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from api.models import Users
from django import forms
from django.shortcuts import render
from django.contrib import messages

class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['id',
                   'first_name',
                   'last_name', 
                   'email', 
                   ]

class EditUser(View):

    def get(self, request, user_id):
        if request.user.is_superuser:
            usuario = get_object_or_404(Users, id=user_id)
            form = UserForm(instance=usuario)
            return render(request, 'editar_Usuario.html', {'form': form,
                                                          'usuario': usuario})
        else:
            return render(request, '404.html', {
                'status_code': 403,
                'error_message': 'Parece que no estás autorizado.'
            }, status=403)
        

    def post(self, request, user_id):
        user = get_object_or_404(Users, id=user_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'El usuario se ha actualizado correctamente.')
            return redirect('usuarios')
        else:
        # En caso de que el formulario no sea válido, devolvemos al usuario al formulario con los errores
            messages.error(request, 'Parece que ha ocurrido un error al actualizar el usuario. Por favor, revisa los campos e inténtalo de nuevo.')
            return redirect('usuarios')