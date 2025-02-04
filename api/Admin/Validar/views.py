from api.models import requisicion, utensilios, RequisicionItem
from rest_framework.views import APIView
from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages

class ValidarRequisicionView(APIView):
    template_name = 'validar_requisicion.html'

    def get(self, request, id):
        requisicion_obj = get_object_or_404(requisicion, id=id)
        
        utensilios_list = utensilios.objects.all()
        search_query = request.GET.get('search', '')
        
        if search_query:
            utensilios_list = utensilios.objects.filter(nombre__icontains=search_query)
        
        paginator = Paginator(utensilios_list, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'requisicion': requisicion_obj,
            'utensilios': requisicion_obj.items,
            'page_obj': page_obj,
            'search_query': search_query 
        }
        return render(request, self.template_name, context)
    
    def post(self, request, id):
        requisicion_id = request.POST.get('requisicion_id')
        requisicion_obj = get_object_or_404(requisicion, id=requisicion_id)

        # Inicializamos una lista para los utensilios
        utensilios_actualizados = []

        # Revisamos cuántos utensilios han sido enviados (basado en el índice de la lista)
        utensilios_count = len(request.POST.getlist('utensilios[0][id]'))  # Verifica cuántos utensilios

        # Iteramos sobre cada utensilio
        for i in range(utensilios_count):
            # Obtenemos los valores de cada utensilio por índice
            item_id = request.POST.get(f'utensilios[{i}][id]')
            estado = request.POST.get(f'utensilios[{i}][estado]')
            entrega = request.POST.get(f'utensilios[{i}][entrega]')

            # Añadimos el utensilio actualizado a la lista
            utensilios_actualizados.append({
                'id': item_id,
                'estado': estado,
                'observaciones': entrega
            })

            # Imprime los datos del utensilio para depuración
            print(f"Item ID: {item_id}, Estado: {estado}, Entrega: {entrega}")

            # Verificamos si el estado es None y asignamos un valor predeterminado
            if not estado:
                estado = 'no_entregado'

            # Buscamos el RequisicionItem correspondiente
            requisicion_item = RequisicionItem.objects.filter(
                requisicion=requisicion_obj,
                item_id=item_id
            ).first()

            if requisicion_item:
                # Si el item existe, actualizamos su estado y cantidad
                requisicion_item.estado = estado
                requisicion_item.observaciones = entrega
                requisicion_item.save()
                print(f"Se actualizó el estado del item {item_id} a: {estado} y cantidad a: {entrega}")
            else:
                return JsonResponse({'error': f"El item con id {item_id} no se encuentra en esta requisición."}, status=400)

        messages.success(request, "Requisición actualizada correctamente.")
        return redirect('HistoryAdmn')
