from rest_framework import viewsets, serializers
from core.models import Community
from .utils import BasePathSerializer


class CommunityPathSerializer(BasePathSerializer):
    zona_a = serializers.StringRelatedField(many=False, source="zone")
    zona_b = serializers.StringRelatedField(many=False, source="zone_2")

    @staticmethod
    def get_path():
        return "communities"

    class Meta:
        model = Community
        fields = [
            "name",
            "url",
            "zona_a",
            "zona_b",
            "zone",
            "zone_2",
            "url"
        ]

        custom_kwargs = {
            "zone": {"hidden": True},
            "zone_2": {"hidden": True},
        }
        extra_kwargs = {
            "zone": {"write_only": True},
            "zone_2": {"write_only": True},
        }

class CommunityDetailsPathSerializer(BasePathSerializer):
    zona_a = serializers.StringRelatedField(many=False, source="zone")
    zona_b = serializers.StringRelatedField(many=False, source="zone_2")

    @staticmethod
    def get_path():
        return "communities"

    class Meta:
        model = Community
        fields = [
            "name",
            "url",
            "zona_a",
            "zona_b",
            "zone",
            "zone_2",
            "url"
        ]

        custom_kwargs = {
            "zone": {"hidden": True},
            "zone_2": {"hidden": True},
        }
 

class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.select_related("zone", "zone_2").all()
    serializer_class = CommunityPathSerializer
    serializer_details_class = CommunityDetailsPathSerializer
    
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = self.serializer_details_class
        return super().retrieve(request, *args, **kwargs)