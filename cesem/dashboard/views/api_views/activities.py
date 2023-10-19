from rest_framework import viewsets, serializers
from core.models import Activity
from .utils import BasePathSerializer


class ActivityPathSerializer(BasePathSerializer):
    superior = serializers.SerializerMethodField()

    def get_superior(self, obj):
        if obj.parent:
            return obj.parent.position
        return ''

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
