import json
from multiprocessing import util
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import logging
from rest_framework import generics, status, response
from django.views.decorators.csrf import csrf_exempt
import requests
import empresas
from .models import Usuario  # Asegúrate de importar tu modelo
from empresas.models import Credenciales_Empresa, Empresa  # Importa los modelos correctos

logger = logging.getLogger(__name__)
API_TOKEN ="7850AHMCUMROS792O012092928391" 
appId="530977999838510"
# Vista para renderizar la página principal
# Devuelve la plantilla de la página de inicio o un error en caso de fallo.
def home(request):
    """
    Renderiza la página principal del sitio.

    :param request: Objeto HttpRequest que contiene los metadatos de la solicitud.
    :return: HttpResponse con la plantilla renderizada o mensaje de error.
    """
    try:
        return render(request, 'inicio/index.html')
    except Exception as e:
        logger.error(f"Error al renderizar la página principal: {str(e)}")
        return HttpResponse("Error interno del servidor.", status=500)

# Vista para manejar el callback embebido.
# Procesa parámetros de registro exitoso o errores.
def embedded_callback(request):
    """
    Maneja el callback embebido verificando los parámetros de registro o error.

    :param request: Objeto HttpRequest que contiene los metadatos de la solicitud.
    :return: HttpResponse con el código de registro o mensaje de error.
    """
    try:
        code = request.GET.get('code')
        error = request.GET.get('error')

        if not code and not error:
            logger.warning("Faltan parámetros obligatorios en el callback.")
            return HttpResponse("Faltan parámetros obligatorios.", status=400)

        if code:
            logger.info(f"Registro exitoso con código: {code}")
            return HttpResponse(f"Registro exitoso con código: {code}")
        elif error:
            logger.warning(f"Error en el registro: {error}")
            return HttpResponse(f"Error en el registro: {error}", status=400)
    except Exception as e:
        logger.error(f"Error inesperado en el callback embebido: {str(e)}")
        return HttpResponse("Error interno del servidor.", status=500)

# Vista para renderizar la página de inicio de sesión.
def login(request):
    """
    Renderiza la página de inicio de sesión.

    :param request: Objeto HttpRequest que contiene los metadatos de la solicitud.
    :return: HttpResponse con la plantilla de inicio de sesión.
    """
    return render(request, 'inicio/login.html')

# Vista para la verificación de WhatsApp.
# Valida el token proporcionado y responde con el reto adecuado.
def whatsapp_verify(request):
    """
    Verifica la autenticidad de las solicitudes de webhook de WhatsApp.

    :param request: Objeto HttpRequest que contiene los metadatos de la solicitud.
    :return: HttpResponse con el reto de verificación o un mensaje de error.
    """
    try:
        logging.debug("Iniciando verificación de WhatsApp.")
        accessToken = "7850AHMCUMROS792O012092928391"  # Ejemplo; NO usar tokens sensibles directamente en el código.
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")
        
        logging.debug(f"Parámetros recibidos: token={token}, challenge={challenge}")
        if token and challenge and token == accessToken:
            logging.info("Verificación de WhatsApp exitosa.")
            return HttpResponse(challenge)

        if token == accessToken:
            logging.info("Token válido, devolviendo challenge.")
            return HttpResponse(challenge)
        else:
            logging.warning("Token de verificación no válido.")
            return HttpResponse("Token de verificación no válido.", status=403)
    except Exception as e:
        logging.error(f"Error inesperado en la verificación de WhatsApp: {str(e)}")
        return HttpResponse("Error interno del servidor.", status=500)

    
#vista para procesar la respuesta despues del registro embebido
# Esta vista se encarga de recibir el token de acceso y otros datos necesarios para la integración con WhatsApp.
@csrf_exempt
def process_token(request):
    """
    Procesa el token recibido desde una solicitud y lo almacena en la tabla Credenciales_Empresa.
    """
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            code = body.get("code")
            empresa_id = body.get("empresa_id")  # Puedes enviar este dato desde el frontend si lo tienes

            if not code:
                return JsonResponse({"error": "Falta el código de autenticación."}, status=400)

            # Intercambiar el code por access_token y otros datos
            url = "https://graph.facebook.com/v21.0/oauth/access_token"
            params = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": "TU_REDIRECT_URI",  # Debe coincidir con el configurado en Facebook
                "client_id": "530977999838510",
                "client_secret": {{API_TOKEN}},
            }
            fb_response = requests.get(url, params=params)
            if fb_response.status_code != 200:
                return JsonResponse({"error": "No se pudo intercambiar el code."}, status=400)
            fb_data = fb_response.json()
            access_token = fb_data.get("access_token")
            token_expiracion = fb_data.get("expires_in", "")  # Si está disponible

            # Aquí puedes hacer otra petición para obtener datos como whatsapp_id, business_id, webhook, etc.
            info_response = requests.get(
                'https://graph.facebook.com/v21.0/me',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            info_data = info_response.json()
            whatsapp_id = info_data.get('id')
            business_id = info_data.get('business_id')

            # Busca la empresa (ajusta la lógica según tu flujo)
            if empresa_id:
                empresa = Empresa.objects.filter(id=empresa_id).first()
            else:
                empresa = Empresa.objects.first()  # O busca por algún parámetro relevante

            if not empresa:
                return JsonResponse({"error": "No se encontró una empresa para asociar el token."}, status=400)

            # Guarda el access_token y otros datos en Credenciales_Empresa
            cred, creado = Credenciales_Empresa.objects.update_or_create(
                Empresa_id=empresa,
                defaults={
                    "access_token": access_token,
                    "token_expiracion": token_expiracion,
                    "whatsapp_id": whatsapp_id,  # Asegúrate de obtener este dato antes
                    "business_id": business_id,  # Descomenta si obtienes este dato
                    # "webhook": "TU_WEBHOOK_URL", # Ajusta según tu lógica
                    "app_id": params["client_id"],
                    "client_secret": params["client_secret"],
                }
            )

            # Comparte la línea de crédito si tienes ambos datos
            if empresa.allocation_configuration_id and cred.whatsapp_id:
                credit_response = share_credit_line_with_customer(empresa, cred.whatsapp_id)
            else:
                credit_response = {"error": "Faltan datos para compartir la línea de crédito."}

            return JsonResponse({
                "success": True,
                "accessToken": access_token,
                "credenciales_id": cred.id,
                "credit_line_response": credit_response
            })

        except Exception as e:
            logger.error(f"Error procesando el token: {str(e)}")
            return JsonResponse({"error": "Error al procesar el token."}, status=500)
    else:
        return HttpResponse("Método no permitido", status=405)
def send_message_view(request):
    # Ejemplo de valores, reemplaza con los reales o dinámicos
    phone_number = "phoneNumber"
    phone_id = "clientId"
    api_token = "clientSecret"

    # Define or import send_welcome_message before using it
    def send_welcome_message(phone_number, phone_id, api_token):
        # Example implementation, replace with actual logic
        return {"success": True, "data": {"phone_number": phone_number, "phone_id": phone_id}}

    result = send_welcome_message(phone_number, phone_id, api_token)
    
    if result["success"]:
        return JsonResponse({"message": "Mensaje enviado con éxito.", "data": result["data"]})
    else:
        return JsonResponse({"error": result["error"]}, status=400)
    
@csrf_exempt
def register_company(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            company_name = body.get("companyName")
            webhook_url = body.get("webhookUrl")
            phone_number = body.get("phoneNumber")
            client_id = body.get("clientId")  # Nuevo parámetro
            client_secret = body.get("clientSecret")  # Nuevo parámetro

            if not company_name or not webhook_url or not phone_number or not client_id or not client_secret:
                return JsonResponse({"error": "Faltan datos requeridos (companyName, webhookUrl, phoneNumber, clientId o clientSecret)."}, status=400)

            # Crear o actualizar el registro en el modelo
            empresa, creado = empresas.objects.update_or_create(
                nombre=company_name,
                defaults={
                    'telefono': phone_number,
                    'client_id': client_id,
                    'client_secret': client_secret,
                }
            )
            logger.debug(f"Datos recibidos: {request.POST}")
            if empresa and creado:
                logger.debug(f"Empresa creada: {empresa.nombre}")
            else:
                 logger.error("Error al crear empresa")
            message = f"La empresa '{company_name}' fue {'registrada' if creado else 'actualizada'} exitosamente."
            return JsonResponse({"message": message}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato de JSON inválido."}, status=400)
        except Exception as e:
            print("Error en el registro:", str(e))
            return JsonResponse({"error": "Ocurrió un error en el servidor."}, status=500)
    else:
        return JsonResponse({"error": "Método no permitido."}, status=405)
    
    
# Vista para obtener el token del cliente
def exchange_token(request):
    code = request.GET.get('code')  # Código obtenido del login embebido
    company_name = request.GET.get('companyName')  # Nombre de la empresa

    if not code or not company_name:
        return JsonResponse({'error': 'Los parámetros "code" y "companyName" son obligatorios.'}, status=400)

    # Obtener la empresa
    try:
        empresa = empresas.objects.get(nombre=company_name)
    except empresas.DoesNotExist:
        return JsonResponse({'error': f"No se encontró la empresa '{company_name}'."}, status=404)

    # Validar que la empresa tenga client_id y client_secret
    if not empresas.client_id or not empresa.client_secret:
        return JsonResponse({'error': 'La empresa no tiene configurados "client_id" o "client_secret".'}, status=400)

    url = 'https://graph.facebook.com/v21.0/oauth/access_token'
    params = {
        'client_id': empresa.client_id,
        'client_secret': empresa.client_secret,
        'code': code,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        business_token = data.get('access_token')

        # Actualizar el token en la base de datos
        empresa.access_token = business_token
        empresa.save()

        return JsonResponse({
            'message': f"Token actualizado para la empresa '{company_name}'.",
            'business_token': business_token
        })
    else:
        return JsonResponse({'error': response.json()}, status=response.status_code)
# Vista para registrar un número de teléfono del cliente en mi bd
def register_phone_number(request):
    access_token = request.GET.get('access_token')  # Token del negocio
    phone_number_id = request.GET.get('phone_number_id')  # ID del número de teléfono
    pin = request.GET.get('pin')  # PIN deseado
    company_name = request.GET.get('companyName')  # Nombre de la empresa asociada

    if not access_token or not phone_number_id or not pin or not company_name:
        return JsonResponse({'error': 'Se requieren "access_token", "phone_number_id", "pin" y "companyName".'}, status=400)

    url = f'https://graph.facebook.com/v21.0/{phone_number_id}/register'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    payload = {
        'messaging_product': 'whatsapp',
        'pin': pin,
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        # Guardar el número de teléfono en el modelo Empresa
        empresa, creado = empresas.objects.update_or_create(
            nombre=company_name,
            defaults={'telefono': phone_number_id}
        )

        return JsonResponse({
            'message': f"El número de teléfono fue registrado para la empresa '{company_name}'."
        })
    else:
        return JsonResponse({'error': response.json()}, status=response.status_code)

# Vista para obtener datos del cliente
""" def obtener_datos_cliente(request):

    business_token = request.GET.get('access_token')
    if not business_token:
        return JsonResponse({'error': 'El parámetro "access_token" es obligatorio.'}, status=400)

    # Endpoint para obtener datos del cliente
    url = 'https://graph.facebook.com/v21.0/me'
    headers = {
        'Authorization': f'Bearer {business_token}',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        whatsapp_id = data.get('id')
        nombre = data.get('name')
        email = data.get('email')  # Solo si está disponible

        # Guarda los datos en el modelo
        cliente, creado = empresas.objects.get_or_create(
            whatsapp_id=whatsapp_id,
            defaults={
                'nombre': nombre,
                'email': email,
                'access_token': business_token,
            },
        )

        if not creado:
            cliente.access_token = business_token
            cliente.save()

        return JsonResponse({'success': True, 'cliente': {
            'nombre': cliente.nombre,
            'email': cliente.email,
            'whatsapp_id': cliente.whatsapp_id,
        }})
    else:
        return JsonResponse({'error': response.json()}, status=response.status_code)
 """
#data adicional de los datos cliente 
@csrf_exempt
def guardar_datos_adicionales(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        telefono = body.get('telefono')
        direccion = body.get('direccion')
        whatsapp_id = body.get('whatsapp_id')  # Obtén el ID del cliente del frontend o de la sesión

        if not whatsapp_id:
            return JsonResponse({'error': 'El "whatsapp_id" es obligatorio.'}, status=400)

        # Actualiza el cliente
        try:
            cliente = empresas.objects.get(whatsapp_id=whatsapp_id)
            cliente.telefono = telefono
            cliente.direccion = direccion
            cliente.save()
            return JsonResponse({'success': True})
        except empresas.DoesNotExist:
            return JsonResponse({'error': 'Cliente no encontrado.'}, status=404)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
    

@csrf_exempt
def process_signup_event(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            event_type = body.get('event')  # "FINISH" o "CANCEL"
            data = body.get('data', {})
            
            if event_type == "FINISH":
                phone_number_id = data.get('phone_number_id')
                waba_id = data.get('waba_id')
                
                # Crear o actualizar la empresa con estos datos
                empresa, created = empresas.objects.update_or_create(
                    telefono=phone_number_id,
                    defaults={'client_id': waba_id},
                )
                
                message = "Registro exitoso procesado"
                if created:
                    logger.info(f"Nueva empresa creada con Phone ID: {phone_number_id}, WABA ID: {waba_id}")
                else:
                    logger.info(f"Datos de la empresa actualizados: Phone ID: {phone_number_id}, WABA ID: {waba_id}")
                
                return JsonResponse({"message": message}, status=200)
            
            elif event_type == "CANCEL":
                current_step = data.get('current_step')
                logger.info(f"Flujo abandonado en: {current_step}")
                return JsonResponse({"message": "Flujo abandonado procesado"}, status=200)
            
            else:
                logger.warning("Evento desconocido recibido")
                return JsonResponse({"error": "Evento desconocido"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato de JSON inválido"}, status=400)
        except Exception as e:
            logger.error(f"Error procesando evento: {str(e)}")
            return JsonResponse({"error": "Error interno del servidor"}, status=500)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    
def meta_callback(request):
    """
    Página de respuesta para manejar la redirección tras el flujo embebido.
    """
    try:
        # Obtén los parámetros enviados por Meta
        code = request.GET.get('code')
        error = request.GET.get('error')

        if error:
            logger.warning(f"Error recibido de Meta: {error}")
            return render(request, 'error.html', {'message': 'Hubo un error en el registro embebido.'})

        if code:
            # Aquí puedes guardar o procesar el código
            logger.info(f"Código recibido de Meta: {code}")

            # Redirige o muestra una página personalizada
            return render(request, 'login_access.html', {'code': code})

        # Si no hay parámetros relevantes
        return HttpResponse("No se recibieron datos válidos.", status=400)
    except Exception as e:
        logger.error(f"Error en el callback de Meta: {str(e)}")
        return HttpResponse("Error interno del servidor.", status=500)

import requests

def share_credit_line_with_customer(empresa, whatsapp_id):
    """
    Comparte la línea de crédito de la empresa con el WABA del cliente.
    """
    credit_line_id = empresa.allocation_configuration_id
    access_token = "EAAHi6ZCMQXS4BO4JSkIZC6fzubP0sZBlnTH0C5gZB11fjuGM8R1otyh6QQnisxtivLnEX4fuhbcoJZBOtayHwuOll6JuFegZCxMZAPbgBUIrJqd58P1uyc9vAkQDs2q4bsxTrNcnV73wPD0gqXDFGHiRteZCjOCgKwVqrSoALBEBpAffhJ2g0TiNz0u1Wu1To0qovwZDZD"  # Usa el token de tu usuario del sistema de Meta
    url = f"https://graph.facebook.com/v21.0/{credit_line_id}/shared_credit"
    payload = {
        "waba_id": whatsapp_id,
        "access_token": access_token
    }
    response = requests.post(url, data=payload)
    return response.json()

