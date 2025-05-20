from django.shortcuts import render# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.conf import settings
from .serializers import WhatsAppWebhookSerializer, MessageTestSerializer
from .services.whatsapp import whatsapp_service
from .services.message_handler import handle_incoming_message
from drf_yasg.views import get_schema_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponse
import os
WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "default_token")

class VerifyWebhookView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="hub.mode",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Mode of the webhook verification"
            ),
            openapi.Parameter(
                name="hub.verify_token",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Verification token"
            ),
            openapi.Parameter(
                name="hub.challenge",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Challenge token to validate the request"
            ),
        ],
        responses={
            200: "Plain text response",
            400: "Missing required parameters",
            403: "Invalid verify token",
        }
    )
    def get(self, request):
        """
        Verifies the Meta webhook subscription.
        """
        hub_mode = request.query_params.get('hub.mode')
        hub_verify_token = request.query_params.get('hub.verify_token')
        hub_challenge = request.query_params.get('hub.challenge')

        if not all([hub_mode, hub_verify_token, hub_challenge]):
            return Response({"error": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)

        if hub_mode == "subscribe" and hub_verify_token == "Claro2025":
            #return Response(hub_challenge, content_type="text/plain", status=status.HTTP_200_OK)
            return HttpResponse(hub_challenge, content_type="text/plain", status=status.HTTP_200_OK)
        

        return Response({"error": "Invalid verify token"}, status=status.HTTP_403_FORBIDDEN)

class WhatsAppWebhookView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=WhatsAppWebhookSerializer,
        responses={
            200: openapi.Response("Success response", openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "status": openapi.Schema(type=openapi.TYPE_STRING, description="Processing status"),
                },
            )),
            400: openapi.Response("Invalid payload", openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING),
                    "details": openapi.Schema(type=openapi.TYPE_OBJECT),
                },
            )),
        }
    )
    def post(self, request):
        """
        Recibe notificaciones de WhatsApp y procesa mensajes entrantes.
        """
        serializer = WhatsAppWebhookSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": "Invalid payload", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        entry = data.get('entry', [{}])[0]
        changes = entry.get('changes', [{}])[0]
        value = changes.get('value', {})

        messages = value.get('messages', [])
        contacts = value.get('contacts', [])


        if messages and contacts:
            message = messages[0]
            sender_info = contacts[0]
            try:
                handle_incoming_message(message, sender_info)
                return Response({"status": "Message processed successfully"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": "Error processing message", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"status": "No messages to process"}, status=status.HTTP_200_OK)


class TestMessageView(APIView):

    @swagger_auto_schema(
        request_body=MessageTestSerializer,
        responses={
            200: openapi.Response("Message sent successfully", openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    "message": openapi.Schema(type=openapi.TYPE_STRING),
                    "response": openapi.Schema(type=openapi.TYPE_OBJECT),
                },
            )),
            400: openapi.Response("Invalid data", openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING),
                    "details": openapi.Schema(type=openapi.TYPE_OBJECT),
                },
            )),
            500: openapi.Response("Failed to send message", openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING),
                },
            )),
        }
    )
    def post(self, request):
        """
        Envía un mensaje de prueba a un número de WhatsApp.
        """
        serializer = MessageTestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": "Invalid data", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        response = whatsapp_service.send_message(to=data['phone_number'], body=data['message'])
        
        if not response:
            return Response({"error": "Failed to send message"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response({"success": True, "message": "Message sent successfully", "response": response})
