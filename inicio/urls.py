from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('embedded-callback/', views.embedded_callback, name='embedded_callback'),
    path('login/', views.login, name='login'),
    path('send-message/', views.send_message_view, name='send_message'),
    path('register/', views.register_company, name='register_company'),
    path('exchange-token/', views.exchange_token, name='exchange_token'),
    path('register-phone/', views.register_phone_number, name='register_phone_number'),
    path('process_signup_event/', views.process_signup_event, name='process_signup_event'),
    path('meta-callback/', views.meta_callback, name='meta_callback'),
    #path('webhooks', webhooks.webhooks, name='webhooks'),
    #path('webhook', webhooks.webhook, name='webhook'),
]
