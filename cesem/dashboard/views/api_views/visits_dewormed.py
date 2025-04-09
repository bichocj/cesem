from core.models import VisitAnimalDeworming
from rest_framework import serializers, viewsets

from .utils import BasePathSerializer
from .zones import ZonePathSerializer


class VisitAnimalDewormedPathSerializer(BasePathSerializer):
    zona = serializers.StringRelatedField(many=False, source="production_unit.zone")
    comunidad = serializers.StringRelatedField(
        many=False, source="production_unit.community"
    )
    sector = serializers.StringRelatedField(many=False, source="production_unit.sector")
    up_responsable = serializers.StringRelatedField(
        many=False, source="production_unit.person_responsable"
    )
    cesem_especialista = serializers.StringRelatedField(
        many=False, source="employ_specialist"
    )
    cesem_responsable = serializers.StringRelatedField(
        many=False, source="employ_responsable"
    )
    actividad = serializers.StringRelatedField(many=False, source="activity")

    @staticmethod
    def get_path():
        return "visits-desparasitacion"

    class Meta:
        model = VisitAnimalDeworming
        fields = [
            "visited_at",
            "zona",
            "comunidad",
            "sector",
            "up_responsable",
            "up_member_name",
            "cesem_especialista",
            "cesem_responsable",
            "actividad",
            "v_race",
            "v_dewormed",
            "v_no_dewormed",
            "v_total",
            "o_race",
            "o_dewormed",
            "o_no_dewormed",
            "o_total",
            "a_race",
            "a_dewormed",
            "a_no_dewormed",
            "a_total",
            "l_race",
            "l_dewormed",
            "l_no_dewormed",
            "l_total",
            "c_total",
            "total",
            "url",
        ]


class VisitAnimalDewormingViewSet(viewsets.ModelViewSet):
    queryset = (
        VisitAnimalDeworming.objects.select_related("production_unit")
        .select_related("production_unit__zone")
        .select_related("production_unit__person_responsable")
        .select_related("employ_specialist", "employ_responsable")
        .select_related("activity")
        .all()
    )
    serializer_class = VisitAnimalDewormedPathSerializer

    filterset_fields = {
        "visited_at": ["exact"],
        "production_unit__zone__name": ["icontains"],
        "production_unit__community__name": ["icontains"],
        "production_unit__sector__name": ["icontains"],
        "production_unit__person_responsable__name": ["icontains"],
        "up_member_name": ["icontains"],
        "employ_specialist__name": ["icontains"],
        "employ_responsable__name": ["icontains"],
        "activity__name": ["icontains"],
    }
