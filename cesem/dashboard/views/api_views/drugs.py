from rest_framework import viewsets
from core.models import Drug
from .utils import BasePathSerializer

class DrugPathSerializer(BasePathSerializer):
       
    @staticmethod
    def get_path():
        return 'drugs'
    
    class Meta:
        model = Drug
        fields = ['name', 'um', 'url']
        

class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugPathSerializer
    filterset_fields = {
        'name': ['contains']
    }
