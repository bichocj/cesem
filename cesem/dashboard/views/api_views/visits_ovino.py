from core.models import VisitGeneticImprovementOvino
from rest_framework import serializers, viewsets

from .utils import BasePathSerializer
from .zones import ZonePathSerializer


class VisitGeneticImprovementOvinoPathSerializer(BasePathSerializer):
    zona = serializers.StringRelatedField(many=False, source="production_unit.zone")
    up_responsable = serializers.StringRelatedField(
        many=False, source="production_unit.person_responsable"
    )
    up_miembro = serializers.StringRelatedField(
        many=False, source="up_member"
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
            "up_responsable",
            "up_miembro",
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
        .select_related("up_member")
        .select_related("employ_specialist", "employ_responsable")
        .select_related("activity")
        .all()
    )
    serializer_class = VisitGeneticImprovementOvinoPathSerializer

    filterset_fields = {
        "production_unit__zone__name": ["contains"],
        "production_unit__person_responsable__name": ["contains"],
        "up_member__name": ["contains"],
        "employ_specialist__name": ["contains"],
        "employ_responsable__name": ["contains"],
        "activity__name": ["contains"],
    }
