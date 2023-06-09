from core.models import VisitAnimal
from rest_framework import serializers, viewsets

from .utils import BasePathSerializer
from .zones import ZonePathSerializer


class VisitAnimalPathSerializer(BasePathSerializer):
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
    enfermedad_observación = serializers.StringRelatedField(
        many=False, source="sickness_observation"
    )
    diagnostico = serializers.StringRelatedField(many=False, source="diagnostic")

    @staticmethod
    def get_path():
        return "visits-animals"

    class Meta:
        model = VisitAnimal
        fields = [
            "visited_at",
            "zona",
            "up_responsable",
            "up_miembro",
            "cesem_especialista",
            "cesem_responsable",
            "actividad",
            "enfermedad_observación",
            "diagnostico",
            "vacunos",
            "ovinos",
            "alpacas",
            "llamas",
            "canes",
            "url",
        ]


class VisitAnimalViewSet(viewsets.ModelViewSet):
    queryset = (
        VisitAnimal.objects.select_related("production_unit")
        .select_related("production_unit__zone")
        .select_related("production_unit__person_responsable")
        .select_related("production_unit__person_member")
        .select_related("employ_specialist", "employ_responsable")
        .select_related("activity")
        .select_related("sickness_observation")
        .select_related("diagnostic")
        .all()
    )
    serializer_class = VisitAnimalPathSerializer

    filterset_fields = {
        "production_unit__zone__name": ["contains"],
        "production_unit__person_responsable__name": ["contains"],
        "production_unit__person_member__name": ["contains"],
        "employ_specialist__name": ["contains"],
        "employ_responsable__name": ["contains"],
        "activity__name": ["contains"],
        "sickness_observation__name": ["contains"],
        "diagnostic__name": ["contains"],
    }
