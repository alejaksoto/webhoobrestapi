from rest_framework import serializers

# Definimos una clase `WhatsAppWebhookSerializer` que hereda de `serializers.Serializer`.
# Esta clase se utiliza para validar y estructurar los datos recibidos en un webhook de WhatsApp.
class WhatsAppWebhookSerializer(serializers.Serializer):
    # Definimos un campo llamado `entry`, que es una lista de diccionarios.
    # Este campo es obligatorio (`required=True`) y se utiliza para representar
    # la estructura de datos que WhatsApp envía en su webhook.
    entry = serializers.ListField(child=serializers.DictField(), required=True)

# Definimos otra clase `MessageTestSerializer` que también hereda de `serializers.Serializer`.
# Esta clase se utiliza para validar y estructurar datos relacionados con pruebas de mensajes.
class MessageTestSerializer(serializers.Serializer):
    # Campo `phone_number`: una cadena de texto obligatoria que representa el número de teléfono.
    phone_number = serializers.CharField(required=True)
    # Campo `message`: una cadena de texto obligatoria que representa el contenido del mensaje.
    message = serializers.CharField(required=True)
