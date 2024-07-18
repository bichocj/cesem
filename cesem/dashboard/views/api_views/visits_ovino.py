from core.models import VisitGeneticImprovementOvino
from rest_framework import serializers, viewsets

from .utils import BasePathSerializer
from .zones import ZonePathSerializer


class VisitGeneticImprovementOvinoPathSerializer(BasePathSerializer):
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
        return "visits-ovino"

    class Meta:
        model = VisitGeneticImprovementOvino
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
            "selected_ovines",
            "synchronized_ovines",
            "inseminated_sheeps_corriedale",
            "inseminated_sheeps_criollas",
            "pregnant",
            "empty",
            "not_evaluated",
            "baby_males",
            "baby_females",
            "baby_deaths",
            "course_male_attendance",
            "course_female_attendance",
            "technical_assistance_attendance",
            "ovinos_number",
            "url",
        ]


class VisitGeneticImprovementOvinoViewSet(viewsets.ModelViewSet):
    queryset = (
        VisitGeneticImprovementOvino.objects.select_related("production_unit")
        .select_related("production_unit__zone")
        .select_related("production_unit__person_responsable")
        .select_related("employ_specialist", "employ_responsable")
        .select_related("activity")
        .all()
    )
    serializer_class = VisitGeneticImprovementOvinoPathSerializer

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
