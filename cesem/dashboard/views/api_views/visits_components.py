from core.models import VisitComponents
from rest_framework import serializers, viewsets

from .utils import BasePathSerializer
from .zones import ZonePathSerializer


class VisitComponentsPathSerializer(BasePathSerializer):
    zona = serializers.StringRelatedField(many=False, source="production_unit.zone")
    comunidad = serializers.StringRelatedField(
        many=False, source="production_unit.community"
    )
    sector = serializers.StringRelatedField(many=False, source="production_unit.sector")
    up_responsable = serializers.StringRelatedField(
        many=False, source="production_unit.person_responsable"
    )
    tecnico_cadenas = serializers.StringRelatedField(
        many=False, source="technical_employee"
    )
    especialista_cadenas = serializers.StringRelatedField(
        many=False, source="specialist_employee"
    )
    capacitador = serializers.StringRelatedField(many=False, source="trainer_employee")
    actividad = serializers.StringRelatedField(many=False, source="activity")

    @staticmethod
    def get_path():
        return "visits-components"

    class Meta:
        model = VisitComponents
        fields = [
            "visited_at",
            "parte_number",
            "year",
            "general_data",
            "zona",
            "comunidad",
            "sector",
            "up_responsable",
            "age",
            "tecnico_cadenas",
            "especialista_cadenas",
            "capacitador",
            "actividad",
            "quantity",
            "certificate_delivery",
            "pedagogical_process",
            "url",
        ]


class VisitComponentsViewSet(viewsets.ModelViewSet):
    queryset = (
        VisitComponents.objects.select_related("production_unit")
        .select_related("production_unit__zone")
        .select_related("production_unit__person_responsable")
        .select_related("specialist_employee", "technical_employee", "trainer_employee")
        .select_related("activity")
        .all()
    )
    serializer_class = VisitComponentsPathSerializer

    filterset_fields = {
        "production_unit__zone__name": ["contains"],
        "production_unit__person_responsable__name": ["contains"],
        "specialist_employee__name": ["contains"],
        "technical_employee__name": ["contains"],
        "trainer_employee__name": ["contains"],
        "activity__name": ["contains"],
    }
