from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import CampaniaMarketing, PlantillaMensaje, cliente_cliente
from .serializers import (
    CampaniaMarketingSerializer,
    PlantillaMensajeSerializer,
    ClienteSerializer
)

class CampaniaMarketingViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar campañas de marketing.
    """
    queryset = CampaniaMarketing.objects.all()
    serializer_class = CampaniaMarketingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    @action(detail=True, methods=['get'])
    def plantillas(self, request, pk=None):
        """Obtener las plantillas asociadas a la campaña."""
        campaña = self.get_object()
        plantillas = campaña.plantillas.all()
        serializer = PlantillaMensajeSerializer(plantillas, many=True)
        return Response(serializer.data)


class PlantillaMensajeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar plantillas de mensajes.
    """
    queryset = PlantillaMensaje.objects.all()
    serializer_class = PlantillaMensajeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        errores = CampaniaMarketing.validar_plantilla(serializer.validated_data['cuerpo'])
        if errores:
            return Response({"error": errores}, status=400)
        serializer.save(creada_por=self.request.user)


class ClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar clientes.
    """
    queryset = cliente_cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filtrar clientes por empresa del usuario autenticado."""
        return self.queryset.filter(empresa_id=self.request.user.empresa_id)

    def perform_create(self, serializer):
        serializer.save()
