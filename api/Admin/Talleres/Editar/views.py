from django.shortcuts import get_object_or_404, redirect
from django.views import View
from api.models import Talleres, Semester
from django.shortcuts import render
from django.contrib import messages

class EditarTallerView(View):
    def get(self, request, taller_id):
        taller = get_object_or_404(Talleres, id=taller_id)
        semestre = Semester.objects.all()
        return render(request, 'editar_taller.html',
                       { 'taller': taller,
                        'semestres': semestre
                        
                        })

    def post(self, request, taller_id):
        taller = get_object_or_404(Talleres, id=taller_id)

        
        # Actualizar los atributos del taller
        taller.name = request.POST.get('nombre')  # Cambiado de 'name' a 'nombre' para que coincida con tu modelo
        taller.semester_id = request.POST.get('semester')  # Si semester es un ForeignKey

        try:
            taller.save()
            messages.success(request, "Taller editado correctamente.")  # Mensaje de éxito
            return redirect('talleres')
        except Exception as e:
            messages.error(request, "Ocurrió un error al editar el taller: " + str(e))  # Mensaje de error
            return redirect('talleres')
  
    
        