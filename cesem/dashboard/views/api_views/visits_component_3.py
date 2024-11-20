from core.models import VisitComponent2, VisitComponent3
from rest_framework import serializers, viewsets

from .utils import BasePathSerializer
from .zones import ZonePathSerializer


class VisitComponent3PathSerializer(BasePathSerializer):
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
        return "visits-component-3"

    class Meta:
        model = VisitComponent3
        fields = [
            "visited_at",
            "parte_number",
            "month_f",
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
            "url",
        ]


class VisitComponent3ViewSet(viewsets.ModelViewSet):
    queryset = (
        VisitComponent2.objects.select_related("production_unit")
        .select_related("production_unit__zone")
        .select_related("production_unit__person_responsable")
        .select_related("specialist_employee", "technical_employee", "trainer_employee")
        .select_related("activity")
        .all()
    )
    serializer_class = VisitComponent3PathSerializer

    filterset_fields = {
        "visited_at": ["exact"],
        "production_unit__zone__name": ["icontains"],
        "production_unit__community__name": ["icontains"],
        "production_unit__sector__name": ["icontains"],
        "production_unit__person_responsable__name": ["icontains"],
        "specialist_employee__name": ["icontains"],
        "technical_employee__name": ["icontains"],
        "trainer_employee__name": ["icontains"],
        "activity__name": ["icontains"],
    }
