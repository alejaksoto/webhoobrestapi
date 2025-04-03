import requests
from django.conf import settings
import os
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "WHATSAPP_TOKEN")
BUSINESS_PHONE = os.getenv("BUSINESS_PHONE", "BUSINESS_PHONE")


class WhatsAppService:
    @staticmethod
    def send_message(to, body):
        url = f'https://graph.facebook.com/v22.0/{BUSINESS_PHONE}/messages'
        headers = {
            "Authorization": f"Bearer {WHATSAPP_TOKEN}",
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
