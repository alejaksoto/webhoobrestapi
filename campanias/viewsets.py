from rest_framework import viewsets

from .serializers import CampaniaMarketingSerializer
from .models import CampaniaMarketing


class CampaniaMarketingViewSet(viewsets.ModelViewSet):
    
    serializer_class = CampaniaMarketingSerializer
    queryset = CampaniaMarketing.objects.all()