from django.db import models

# Create your models here.

class Empresa(models.Model):
    nombre = models.TextField(max_length=255)
    email = models.EmailField(unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)
    fecha_update = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=255)
    allocation_configuration_id = models.TextField(max_length=255,null=True, blank=True)

class Credenciales_Empresa(models.Model):
    Empresa_id = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    whatsapp_id = models.CharField(max_length=255, unique=True)
    access_token = models.TextField()
    token_expiracion = models.TextField()
    webhook = models.TextField()
    app_id = models.CharField(max_length=255, null=True, blank=True)  # Nuevo campo
    client_secret = models.CharField(max_length=255, null=True, blank=True)  # Nuevo campo
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_update = models.DateTimeField(auto_now=True)
    business_id = models.CharField(max_length=255, unique=True)


class LogsEventos(models.Model):
    empresa_id = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    detalle = models.TextField()
    tipo_evento = models.CharField(max_length=50)  # Ejemplo: "error", "advertencia"
    estado = models.CharField(max_length=50)  # Estado del evento
    fecha_creacion = models.DateTimeField(auto_now_add=True)   