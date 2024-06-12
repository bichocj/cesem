from rest_framework import viewsets, serializers
from core.models import Activity
from .utils import BasePathSerializer


class ActivityPathSerializer(BasePathSerializer):
    superior = serializers.SerializerMethodField()

    def get_superior(self, obj):
        if obj.parent:
            return obj.parent.position
        return ""

    @staticmethod
    def get_path():
        return "activities"

    class Meta:
        model = Activity
        fields = (
            "position",
            "name",
            "short_name",
            "um",
            "superior",
            "parent",
            "sum_in_parent",
            "meta_2022",
            "meta_2023",
            "meta_2024",
            "url",
        )
        extra_kwargs = {
            "parent": {"write_only": True},
            # "um": {"write_only": True},
        }


class ActivityDetailsPathSerializer(BasePathSerializer):
    actividad_superior_posicion = serializers.SerializerMethodField()
    actividad_superior_nombre = serializers.StringRelatedField(
        many=False, source="parent"
    )

    def get_actividad_superior_posicion(self, obj):
        if obj.parent:
            return obj.parent.position
        return ""

    @staticmethod
    def get_path():
        return "activities"

    class Meta:
        model = Activity
        fields = (
            "position",
            "name",
            "short_name",
            "um",
            "parent",
            "sum_in_parent",
            "actividad_superior_nombre",
            "actividad_superior_posicion",
            "meta_2022",
            "meta_2023",
            "meta_2024",
            "url",
        )
        extra_kwargs = {
            # "parent": {"write_only": True},
            # "um": {"write_only": True},
        }


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivityPathSerializer
    serializer_details_class = ActivityDetailsPathSerializer
    filterset_fields = {
        "name": ["contains"],        
    }

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = self.serializer_details_class
        return super().retrieve(request, *args, **kwargs)
    
