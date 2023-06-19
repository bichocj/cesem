from core.models import VisitGrass
from rest_framework import serializers, viewsets

from .utils import BasePathSerializer
from .zones import ZonePathSerializer


class VisitGrassPathSerializer(BasePathSerializer):
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
        return "visits-grass"

    class Meta:
        model = VisitGrass
        fields = [
            "visited_at",
            "zona",
            "up_responsable",
            "up_miembro",
            "cesem_especialista",
            "cesem_responsable",
            "actividad",
            "planting_intention_hectares",
            "avena_vicia_planted_hectares",
            "alfalfa_dactylis_planted_hectares",
            "raygrass_trebol_planted_hectares",
            "direct_grazing",
            "hay",
            "ensilage",
            "bale",
            "perennial_grazing",
            "perennial_yield",
            "url",
        ]


class VisitGrassQuantityPathSerializer(BasePathSerializer):
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
        return "visits-grass"

    class Meta:
        model = VisitGrass
        fields = [
            "visited_at",
            "zona",
            "up_responsable",
            "up_miembro",
            "cesem_especialista",
            "cesem_responsable",
            "actividad",
            "quantity",
            "url",
        ]


class VisitGrassViewSet(viewsets.ModelViewSet):
    queryset = (
        VisitGrass.objects.select_related("production_unit")
        .select_related("production_unit__zone")
        .select_related("production_unit__person_responsable")
        .select_related("production_unit__person_member")
        .select_related("employ_specialist", "employ_responsable")
        .select_related("activity")
        .all()
    )
    serializer_class = VisitGrassPathSerializer
    serializer_quantity_class = VisitGrassQuantityPathSerializer

    filterset_fields = {
        "production_unit__zone__name": ["contains"],
        "production_unit__person_responsable__name": ["contains"],
        "production_unit__person_member__name": ["contains"],
        "employ_specialist__name": ["contains"],
        "employ_responsable__name": ["contains"],
        "activity__name": ["contains"],
    }

    def retrieve(self, request, *args, **kwargs):
        if self.get_object().quantity > 0:
            self.serializer_class = self.serializer_quantity_class
        return super().retrieve(request, *args, **kwargs)
