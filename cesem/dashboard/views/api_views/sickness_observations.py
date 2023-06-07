from rest_framework import viewsets
from core.models import SicknessObservation
from .utils import BasePathSerializer

class SicknessObservationPathSerializer(BasePathSerializer):
       
    @staticmethod
    def get_path():
        return 'sickness_observations'
    
    class Meta:
        model = SicknessObservation
        fields = ['name', 'url']
        

class SicknessObservationViewSet(viewsets.ModelViewSet):
    queryset = SicknessObservation.objects.all()
    serializer_class = SicknessObservationPathSerializer
    filterset_fields = {
        'name': ['contains']
    }
