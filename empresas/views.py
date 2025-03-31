import requests
from django.http import JsonResponse
from django.conf import settings
from django.views import View
from .models import Empresa, Credenciales_Empresa

class ShareCreditLineView(View):
    def post(self, request, extended_credit_line_id):
        # Obtener el identificador de la empresa (esto podría venir como un parámetro)
        empresa_id = request.POST.get('empresa_id')
        
        if not empresa_id:
            return JsonResponse({'error': 'Se debe proporcionar un id de empresa.'}, status=400)

        try:
            # Obtener la empresa y sus credenciales asociadas
            empresa = Empresa.objects.get(id=empresa_id)
            credenciales = Credenciales_Empresa.objects.get(Empresa_id=empresa)
        except Empresa.DoesNotExist:
            return JsonResponse({'error': 'Empresa no encontrada.'}, status=404)
        except Credenciales_Empresa.DoesNotExist:
            return JsonResponse({'error': 'Credenciales de la empresa no encontradas.'}, status=404)

        # Verificar que la empresa tenga una configuración de asignación (opcional)
        allocation_config_id = empresa.allocation_configuration_id
        if not allocation_config_id:
            return JsonResponse({'error': 'La empresa no tiene una configuración de asignación.'}, status=400)

        # Obtener los parámetros de la solicitud (como la moneda)
        waba_currency = request.POST.get('waba_currency')
        if not waba_currency:
            return JsonResponse({'error': 'Se debe proporcionar la moneda de la empresa (waba_currency).'}, status=400)

        # Definir la URL de la API de WhatsApp Business y los parámetros necesarios
        api_url = f"https://graph.facebook.com/v.21/{extended_credit_line_id}/whatsapp_credit_sharing_and_attach"
        headers = {
            'Authorization': f'Bearer {credenciales.access_token}',
        }
        params = {
            'waba_currency': waba_currency,
            'waba_id': credenciales.whatsapp_id,
        }

        # Realizar la solicitud POST a la API de WhatsApp Business
        try:
            response = requests.post(api_url, headers=headers, params=params)
            response.raise_for_status()  # Lanza un error si la respuesta es 4xx/5xx
            data = response.json()

            # Actualizar el campo de configuración de asignación en la empresa
            empresa.allocation_configuration_id = data.get('allocation_config_id')
            empresa.save()

            # Retornar la respuesta de la API
            return JsonResponse({
                'allocation_config_id': data.get('allocation_config_id'),
                'waba_id': data.get('waba_id'),
            })

        except requests.exceptions.RequestException as e:
            # En caso de error, retornar un mensaje adecuado
            return JsonResponse({'error': str(e)}, status=500)
