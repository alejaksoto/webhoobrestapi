from rest_framework import viewsets

from .serializers import EmpresaSerializer
from .models import Empresa


class EmpresaViewSet(viewsets.ModelViewSet):
    
    serializer_class = EmpresaSerializer
    queryset = Empresa.objects.all()