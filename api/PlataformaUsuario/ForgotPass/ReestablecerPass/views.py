from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from api.models import Users

class PasswordResetConfirmView(View):
    template_name = 'password_reset_confirm.html'

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Users.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                form = SetPasswordForm(user=user)
                return render(request, self.template_name, {'form': form})
            else:
                messages.error(request, 'El enlace para restablecer la contraseña es inválido o ha expirado.')
                return redirect('password_reset')
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            messages.error(request, 'El enlace para restablecer la contraseña es inválido o ha expirado.')
            return redirect('password_reset')

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Users.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                form = SetPasswordForm(user=user, data=request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Tu contraseña ha sido restablecida con éxito.')
                    return redirect('password_reset_complete')
                else:
                    return render(request, self.template_name, {'form': form})
            else:
                messages.error(request, 'El enlace para restablecer la contraseña es inválido o ha expirado.')
                return redirect('password_reset')
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            messages.error(request, 'El enlace para restablecer la contraseña es inválido o ha expirado.')
            return redirect('password_reset')
