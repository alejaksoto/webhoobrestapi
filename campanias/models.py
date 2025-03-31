from django.db import models
from empresas.models import Empresa
from inicio.models import Usuario  

class CampaniaMarketing(models.Model):
    nombre = models.CharField(max_length=255)
    empresa_id = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_update = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="campanias")
    estado = models.BooleanField(default=True)
    lenguaje = models.CharField(max_length=255)

    def validar_plantilla(plantilla_texto):
        import re
        errores = []

        # Validación de llaves disparejas
        if re.search(r"\{\{[^\d]+\}\}", plantilla_texto):
            errores.append("Faltan parámetros o las llaves están disparejas.")

        # Validación de caracteres no permitidos
        if re.search(r"[#$%]", plantilla_texto):
            errores.append("Los parámetros no deben contener caracteres especiales (#, $, %).")

        # Validación de parámetros no secuenciales
        parametros = re.findall(r"\{\{(\d+)\}\}", plantilla_texto)
        secuencia_correcta = list(map(str, range(1, len(parametros) + 1)))
        if parametros != secuencia_correcta:
            errores.append("Los parámetros deben ser secuenciales.")

        return errores

class CategoriaPlantilla(models.Model):
    nombre = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class PlantillaMensaje(models.Model):
    nombre = models.CharField(max_length=255)
    cuerpo = models.TextField()
    lenguaje = models.CharField(max_length=255)
    campaña_id = models.ForeignKey(CampaniaMarketing, on_delete=models.CASCADE, related_name="plantillas")
    es_aprobada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creada_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    categoria_id = models.ForeignKey(CategoriaPlantilla, on_delete=models.CASCADE, related_name="categorias")
    def clean(self):
        from django.core.exceptions import ValidationError
        import re
        
        # Validación: No terminar con parámetros
        if self.cuerpo.strip().endswith("{{"):
            raise ValidationError("La plantilla no puede finalizar con un parámetro.")
        
        # Validación: Parámetros disparejos o no secuenciales
        parametros = re.findall(r"\{\{(\d+)\}\}", self.cuerpo)
        secuencia_correcta = list(map(str, range(1, len(parametros) + 1)))
        if parametros != secuencia_correcta:
            raise ValidationError("Los parámetros deben ser secuenciales y correctos.")
        
class cliente_cliente(models.Model):
    empresa_id = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    nombre = models.CharField(max_length=255)
    numerocel_cliente = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_update = models.DateTimeField(auto_now_add=True)