from rest_framework import serializers
from .models import CampaniaMarketing

class CampaniaMarketingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaniaMarketing
        fields = '__all__'