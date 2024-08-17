from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.views import APIView
from api.models import Users
from django import forms

class UserForm(forms.ModelForm):
    profile_photo = forms.ImageField(label="usuario", required=False, widget=forms.FileInput(attrs={'class': 'user'}))
    
    class Meta:
        model = Users
        fields = ['first_name', 
                  'last_name', 
                  'email', 
                  'profile_photo', 
                  'matricula',
                  'grupo'
                  ]

class info(APIView):
    template_name = "info_usuario.html"
    
    def get(self, request):
        usuario = request.user
        form = UserForm(instance=usuario)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        usuario = request.user
        form = UserForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.save()
            return redirect('info')  # Asegúrate de que esta URL esté definida correctamente
        return render(request, self.template_name, {'form': form})
