from rest_framework import viewsets, serializers
from core.models import Activity
from .utils import BasePathSerializer


class ActivityPathSerializer(BasePathSerializer):
    relacionado = serializers.StringRelatedField(many=False, source="parent.position")

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
            "relacionado",
            "url",
        )
        extra_kwargs = {
            # "parent": {"write_only": True},
            # "um": {"write_only": True},
        }


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivityPathSerializer
