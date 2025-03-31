from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShareCreditLineView
from .viewsets import EmpresaViewSet


router = DefaultRouter()
router.register('empresas', EmpresaViewSet)
urlpatterns = [
    path('share-credit-line/<int:extended_credit_line_id>/', ShareCreditLineView.as_view(), name='share_credit_line'),
]


urlpatterns = router.urls