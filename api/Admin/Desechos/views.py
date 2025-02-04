from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

class Desechos(APIView):

    def post(self, request):

        litros = request.data.get('litros')