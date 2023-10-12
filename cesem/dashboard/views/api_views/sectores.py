from rest_framework import viewsets, serializers
from core.models import Sector
from .utils import BasePathSerializer

class SectorPathSerializer(BasePathSerializer):
    comunidad = serializers.StringRelatedField(many=False, source='community')
    comunidad_2 = serializers.StringRelatedField(many=False, source='community_2')
    comunidad_3 = serializers.StringRelatedField(many=False, source='community_3')
       
    @staticmethod
    def get_path():
        return 'sectors'
    
    class Meta:
        model = Sector
        fields = ['name', 'comunidad', 'comunidad_2', 'comunidad_3', 'community','community_2', 'community_3', 'url', ]
        extra_kwargs = {
            'community': {'write_only': True},
            'community_2': {'write_only': True},
            'community_3': {'write_only': True},
        }
        

class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.select_related('community').all()
    serializer_class = SectorPathSerializer
 
