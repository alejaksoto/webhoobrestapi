from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import CampaniaMarketingViewSet


router = DefaultRouter()
router.register('Campanias', CampaniaMarketingViewSet)


urlpatterns = router.urls