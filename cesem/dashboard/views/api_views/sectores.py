from rest_framework import viewsets, serializers
from core.models import Sector
from .utils import BasePathSerializer

class SectorPathSerializer(BasePathSerializer):
    comunidad = serializers.StringRelatedField(many=False, source='community')
       
    @staticmethod
    def get_path():
        return 'sectors'
    
    class Meta:
        model = Sector
        fields = ['name', 'url', 'comunidad', 'community']
        extra_kwargs = {
            'community': {'write_only': True},
        }
        

class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.select_related('community').all()
    serializer_class = SectorPathSerializer
 
