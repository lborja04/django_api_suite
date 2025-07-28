from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid

# Simulación de base de datos local
data_list = [
    {'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True},
    {'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True},
    {'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False},
]

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
        # Filtra la lista para incluir solo los elementos donde 'is_active' es True
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        # Validación mínima
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)
        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)

class DemoRestApiItem(APIView):
    def put(self, request, item_id):
        for item in data_list:
            if item["id"] == item_id:
                item["name"] = request.data.get("name", "")
                item["email"] = request.data.get("email", "")
                item["is_active"] = request.data.get("is_active", False)
                return Response(
                    {"message": "Elemento actualizado completamente."},
                    status=status.HTTP_200_OK
                )
        return Response(
            {"message": "Elemento no encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )

    def patch(self, request, item_id):
        for item in data_list:
            if item["id"] == item_id:
                item.update({k: v for k, v in request.data.items() if k in item})
                return Response(
                    {"message": "Elemento actualizado parcialmente."},
                    status=status.HTTP_200_OK
                )
        return Response(
            {"message": "Elemento no encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )

    def delete(self, request, item_id):
        for item in data_list:
            if item["id"] == item_id:
                item["is_active"] = False  # Eliminación lógica
                return Response(
                    {"message": "Elemento desactivado correctamente."},
                    status=status.HTTP_200_OK
                )
        return Response(
            {"message": "Elemento no encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )
