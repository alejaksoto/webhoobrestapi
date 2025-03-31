import requests
from django.conf import settings

class WhatsAppService:
    @staticmethod
    def send_message(to, body):
        url = "https://graph.facebook.com/v22.0/{BUSINESS_PHONE}/messages".format(settings.WHATSAPP_BUSINESS_ID)
        headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": body}
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json() if response.status_code == 200 else None

whatsapp_service = WhatsAppService()
