from rest_framework import viewsets
from core.models import Diagnostic
from .utils import BasePathSerializer

class DiagnosticPathSerializer(BasePathSerializer):
       
    @staticmethod
    def get_path():
        return 'diagnostics'
    
    class Meta:
        model = Diagnostic
        fields = ['name', 'url']
        

class DiagnosticViewSet(viewsets.ModelViewSet):
    queryset = Diagnostic.objects.all()
    serializer_class = DiagnosticPathSerializer
    filterset_fields = {
        'name': ['contains']
    }
