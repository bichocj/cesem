from core.models import ProductionUnit, VisitGrass
from dashboard.views.api_views.helper import UpSerializer
from rest_framework import serializers, viewsets

from .utils import BasePathSerializer
from .zones import ZonePathSerializer


class VisitGrassPathSerializer(BasePathSerializer):
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
    actividad_ = serializers.StringRelatedField(many=False, source="activity")

    @staticmethod
    def get_path():
        return "visits-grass"

    class Meta:
        model = VisitGrass
        fields = [
            "visited_at",
            "zona",
            "comunidad",
            "sector",
            "up_responsable",
            "up_member_name",
            "cesem_especialista",
            "cesem_responsable",
            "actividad_",
            "employ_specialist",
            "employ_responsable",
            "production_unit",
            "activity",
            "planting_intention_hectares",
            "ground_analysis",
            "plow_hours",
            "dredge_hours",
            "oat_kg",
            "vicia_kg",
            "alfalfa_kg",
            "dactylis_kg",
            "ryegrass_kg",
            "trebol_b_kg",
            "fertilizer",
            "avena_planted_hectares",
            "avena_vicia_planted_hectares",
            "alfalfa_dactylis_planted_hectares",
            "ryegrass_trebol_planted_hectares",
            "anual_yield",
            "technical_assistance",
            "direct_grazing",
            "hay",
            "ensilage",
            "bale",
            "perennial_grazing",
            "perennial_ensilage",
            "perennial_yield",
            "technical_training_perennial",
            "technical_training_anual",
            "technical_training_conservation",
            "url",
        ]


class VisitGrassDetailPathSerializer(BasePathSerializer):
    cesem_especialista = serializers.StringRelatedField(
        many=False, source="employ_specialist"
    )
    cesem_responsable = serializers.StringRelatedField(
        many=False, source="employ_responsable"
    )
    actividad_ = serializers.StringRelatedField(many=False, source="activity")
    up = serializers.SerializerMethodField()

    def get_up(self, obj):
        serializer = UpSerializer(instance=obj, many=False)
        return serializer.data

    @staticmethod
    def get_path():
        return "visits-grass"

    class Meta:
        model = VisitGrass
        fields = [
            "visited_at",
            "production_unit",
            "up",
            "up_member_name",
            "employ_specialist",
            "cesem_especialista",
            "employ_responsable",
            "cesem_responsable",
            "activity",
            "actividad_",
            "planting_intention_hectares",
            "ground_analysis",
            "plow_hours",
            "dredge_hours",
            "oat_kg",
            "vicia_kg",
            "alfalfa_kg",
            "dactylis_kg",
            "ryegrass_kg",
            "trebol_b_kg",
            "fertilizer",
            "avena_planted_hectares",
            "avena_vicia_planted_hectares",
            "alfalfa_dactylis_planted_hectares",
            "ryegrass_trebol_planted_hectares",
            "anual_yield",
            "technical_assistance",
            "direct_grazing",
            "hay",
            "ensilage",
            "bale",
            "perennial_grazing",
            "perennial_ensilage",
            "perennial_yield",
            "technical_training_perennial",
            "technical_training_anual",
            "technical_training_conservation",
        ]


class VisitGrassViewSet(viewsets.ModelViewSet):
    queryset = (
        VisitGrass.objects.select_related("production_unit")
        .select_related("production_unit__zone")
        .select_related("production_unit__person_responsable")
        .select_related("employ_specialist", "employ_responsable")
        .select_related("activity")
        .all().order_by('-visited_at')
    )
    serializer_class = VisitGrassPathSerializer
    serializer_detail_class = VisitGrassDetailPathSerializer

    def perform_update(self, serializer):
        production_unit_id = self.request.data.get("production_unit", None)
        production_unit = ProductionUnit.objects.get(id=production_unit_id)
        serializer.save(production_unit=production_unit)

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

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = self.serializer_detail_class
        return super().retrieve(request, *args, **kwargs)
