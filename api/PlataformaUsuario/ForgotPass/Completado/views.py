from django.shortcuts import render
from django.views import View

class PasswordResetCompleteView(View):
    template_name = 'password_reset_complete.html'

    def get(self, request):
        return render(request, self.template_name)
