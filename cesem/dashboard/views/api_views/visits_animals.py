from core.models import VisitAnimalHealth, ProductionUnit
from dashboard.views.api_views.helper import UpSerializer
from rest_framework import serializers, viewsets

from .utils import BasePathSerializer
from .zones import ZonePathSerializer


class VisitAnimalHealthPathSerializer(BasePathSerializer):
    zona = serializers.StringRelatedField(many=False, source="production_unit.zone")
    comunidad = serializers.StringRelatedField(
        many=False, source="production_unit.community"
    )
    sector = serializers.StringRelatedField(many=False, source="production_unit.sector")
    up_responsable = serializers.StringRelatedField(
        many=False, source="production_unit.person_responsable"
    )
    up_miembro = serializers.StringRelatedField(many=False, source="up_member")
    cesem_especialista = serializers.StringRelatedField(
        many=False, source="employ_specialist"
    )
    cesem_responsable = serializers.StringRelatedField(
        many=False, source="employ_responsable"
    )
    actividad_ = serializers.StringRelatedField(many=False, source="activity")
    enfermedad_observación = serializers.StringRelatedField(
        many=False, source="sickness_observation"
    )
    diagnostico = serializers.StringRelatedField(many=False, source="diagnostic")

    @staticmethod
    def get_path():
        return "visits-animals"

    class Meta:
        model = VisitAnimalHealth
        fields = [
            "visited_at",
            "production_unit",
            "zona",
            "comunidad",
            "sector",
            "up_responsable",
            "up_miembro",
            
            "employ_specialist",
            "cesem_especialista",
            
            "employ_responsable",
            "cesem_responsable",
            
            "activity",
            "actividad_",
            
            "sickness_observation",
            "enfermedad_observación",
            
            "diagnostic",
            "diagnostico",

            "vacunos",
            "ovinos",
            "alpacas",
            "llamas",
            "canes",
            "url",
        ]
     

class VisitAnimalHealthDetailsPathSerializer(BasePathSerializer):

    up_miembro = serializers.StringRelatedField(many=False, source="up_member")
    cesem_especialista = serializers.StringRelatedField(
        many=False, source="employ_specialist"
    )
    cesem_responsable = serializers.StringRelatedField(
        many=False, source="employ_responsable"
    )
    actividad_ = serializers.StringRelatedField(many=False, source="activity")
    enfermedad_observación_ = serializers.StringRelatedField(
        many=False, source="sickness_observation"
    )
    diagnostico_ = serializers.StringRelatedField(many=False, source="diagnostic")
    up = serializers.SerializerMethodField()

    def get_up(self, obj):
        serializer = UpSerializer(instance=obj, many=False)
        return serializer.data

    @staticmethod
    def get_path():
        return "visits-animals"

    class Meta:
        model = VisitAnimalHealth
        fields = [
            "visited_at",
            'production_unit',
            'up',
            "up_miembro",
            
            "employ_specialist",
            "cesem_especialista",

            "employ_responsable",
            "cesem_responsable",
            
            "activity",
            "actividad_",

            "sickness_observation",
            "enfermedad_observación_",
            
            "diagnostic",
            "diagnostico_",
            
            "vacunos",
            "ovinos",
            "alpacas",
            "llamas",
            "canes",
            "url",
        ]


class VisitAnimalHealthViewSet(viewsets.ModelViewSet):
    queryset = (
        VisitAnimalHealth.objects.select_related("production_unit")
        .select_related("production_unit__zone")
        .select_related("production_unit__person_responsable")
        .select_related("up_member")
        .select_related("employ_specialist", "employ_responsable")
        .select_related("activity")
        .select_related("sickness_observation")
        .select_related("diagnostic")
        .all().order_by('-visited_at')
    )
    serializer_class = VisitAnimalHealthPathSerializer
    serializer_details_class = VisitAnimalHealthDetailsPathSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = self.serializer_details_class
        return super().retrieve(request, *args, **kwargs)
    
    def perform_update(self, serializer):                
        production_unit_id = self.request.data.get("production_unit", None)
        production_unit = ProductionUnit.objects.get(id=production_unit_id)
        serializer.save(production_unit=production_unit)
        

    filterset_fields = {
        "production_unit__zone__name": ["contains"],
        "production_unit__person_responsable__name": ["contains"],
        "up_member__name": ["contains"],
        "employ_specialist__name": ["contains"],
        "employ_responsable__name": ["contains"],
        "activity__name": ["contains"],
        "sickness_observation__name": ["contains"],
        "diagnostic__name": ["contains"],
    }
