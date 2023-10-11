from rest_framework import viewsets, serializers
from core.models import Community
from .utils import BasePathSerializer

class CommunityPathSerializer(BasePathSerializer):
    zona = serializers.StringRelatedField(many=False, source='zone')
       
    @staticmethod
    def get_path():
        return 'communities'
    
    class Meta:
        model = Community
        fields = ['name', 'url', 'zona', 'zone', 'zone_2']
        extra_kwargs = {
           'zone': {'write_only': True},
        }
        

class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.select_related('zone', 'zone_2').all()
    serializer_class = CommunityPathSerializer
