from rest_framework import viewsets, serializers
from core.models import Activity
from .utils import BasePathSerializer


class ActivityPathSerializer(BasePathSerializer):
    superior = serializers.SerializerMethodField()
    importar_excel_como = serializers.SerializerMethodField()

    def get_superior(self, obj):
        if obj.parent:
            return obj.parent.position
        return ""
    
    def get_importar_excel_como(self, obj):
        return obj.get_import_in_display() if obj.import_in is not None else None


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
            "import_in",
            "importar_excel_como",
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
    importar_excel_como = serializers.SerializerMethodField()

    def get_actividad_superior_posicion(self, obj):
        if obj.parent:
            return obj.parent.position
        return ""
    
    def get_importar_excel_como(self, obj):
        return obj.get_import_in_display() if obj.import_in is not None else None

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
            "import_in",
            "importar_excel_como",
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
        "name": ["icontains"],        
    }

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = self.serializer_details_class
        return super().retrieve(request, *args, **kwargs)
    
