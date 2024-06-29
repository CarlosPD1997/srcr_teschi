from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
class ForgotPass(APIView):
    template_name="forgot-password.html"
    def get(self, request):
        return render(request, self.template_name)