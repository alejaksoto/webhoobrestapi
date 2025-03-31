from django.urls import path
from .views import VerifyWebhookView, WhatsAppWebhookView, TestMessageView

urlpatterns = [
    path('', VerifyWebhookView.as_view(), name='verify-webhook'),
    path('webhook', WhatsAppWebhookView.as_view(), name='whatsapp-webhook'),
    path('test/message/', TestMessageView.as_view(), name='test-message'),
]