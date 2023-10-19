from rest_framework import viewsets, serializers
from core.models import Sector
from .utils import BasePathSerializer


class SectorPathSerializer(BasePathSerializer):
    comunidad_a = serializers.StringRelatedField(many=False, source="community")
    comunidad_b = serializers.StringRelatedField(many=False, source="community_2")
    comunidad_c = serializers.StringRelatedField(many=False, source="community_3")

    @staticmethod
    def get_path():
        return "sectors"

    class Meta:
        model = Sector
        fields = [
            "name",
            "comunidad_a",
            "comunidad_b",
            "comunidad_c",
            "community",
            "community_2",
            "community_3",
            "url",
        ]
        extra_kwargs = {
            "community": {"write_only": True},
            "community_2": {"write_only": True},
            "community_3": {"write_only": True},
        }

class SectorDetailsPathSerializer(BasePathSerializer):
    comunidad_a = serializers.StringRelatedField(many=False, source="community")
    comunidad_b = serializers.StringRelatedField(many=False, source="community_2")
    comunidad_c = serializers.StringRelatedField(many=False, source="community_3")

    @staticmethod
    def get_path():
        return "sectors"

    class Meta:
        model = Sector
        fields = [
            "name",
            "comunidad_a",
            "comunidad_b",
            "comunidad_c",
            "community",
            "community_2",
            "community_3",
            "url",
        ]

        custom_kwargs = {
            "community": {"hidden": True},
            "community_2": {"hidden": True},
            "community_3": {"hidden": True},
        }


class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.select_related("community").all()
    serializer_class = SectorPathSerializer
    serializer_details_class = SectorDetailsPathSerializer
    
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = self.serializer_details_class
        return super().retrieve(request, *args, **kwargs)
