from rest_framework import viewsets
from core.models import Zone
from .utils import BasePathSerializer

class ZonePathSerializer(BasePathSerializer):
       
    @staticmethod
    def get_path():
        return 'zones'
    
    class Meta:
        model = Zone
        fields = ['name', 'url']
        

class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZonePathSerializer
    filterset_fields = {
        'name': ['contains']
    }
