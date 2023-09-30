from core.models import VisitGeneticImprovementVacuno
from rest_framework import serializers, viewsets

from .utils import BasePathSerializer
from .zones import ZonePathSerializer


class VisitGeneticImprovementVacunoPathSerializer(BasePathSerializer):
    zona = serializers.StringRelatedField(many=False, source="production_unit.zone")
    up_responsable = serializers.StringRelatedField(
        many=False, source="production_unit.person_responsable"
    )
    up_miembro = serializers.StringRelatedField(
        many=False, source="production_unit.person_member"
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
        return "visits-vacuno"

    class Meta:
        model = VisitGeneticImprovementVacuno
        fields = [
            "visited_at",
            "zona",
            "up_responsable",
            "up_miembro",
            "cesem_especialista",
            "cesem_responsable",
            "actividad",
            "bull_name",
            "bull_race",
            "pajilla_type",
            "pajilla_origin",
            "pajillas_number",
            "cow_name",
            "cow_race",
            "service_number",
            "pregnant",
            "empty",
            "birthday",
            "earring_number",
            "baby_name",
            "male",
            "female",
            "death",
            "baby_bull_name",
            "baby_cow_name",
            "male_attendance",
            "female_attendance",
            "technical_assistance_attendance",
            "vacunos_number",
            "url",
        ]


class VisitGeneticImprovementVacunoViewSet(viewsets.ModelViewSet):
    queryset = (
        VisitGeneticImprovementVacuno.objects.select_related("production_unit")
        .select_related("production_unit__zone")
        .select_related("production_unit__person_responsable")
        .select_related("production_unit__person_member")
        .select_related("employ_specialist", "employ_responsable")
        .select_related("activity")
        .all()
    )
    serializer_class = VisitGeneticImprovementVacunoPathSerializer

    filterset_fields = {
        "production_unit__zone__name": ["contains"],
        "production_unit__person_responsable__name": ["contains"],
        "production_unit__person_member__name": ["contains"],
        "employ_specialist__name": ["contains"],
        "employ_responsable__name": ["contains"],
        "activity__name": ["contains"],
    }
