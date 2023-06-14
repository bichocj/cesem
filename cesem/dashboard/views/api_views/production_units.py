from rest_framework import viewsets, serializers
from core.models import ProductionUnit, VisitAnimal, VisitGrass
from .utils import BasePathSerializer


class ProductionUnitPathSerializer(BasePathSerializer):
    zona_nombre = serializers.StringRelatedField(many=False, source="zone")
    comunidad = serializers.StringRelatedField(many=False, source="community")
    sector = serializers.StringRelatedField(many=False)
    responsable = serializers.StringRelatedField(
        many=False, source="person_responsable"
    )
    miembro = serializers.StringRelatedField(many=False, source="person_member")
    tipologia = serializers.StringRelatedField(many=False, source="tipology")
    es_pilot = serializers.StringRelatedField(many=False, source="is_pilot")

    @staticmethod
    def get_path():
        return "production_units"

    class Meta:
        model = ProductionUnit
        fields = (
            "zona_nombre",
            "zone",
            "comunidad",
            "sector",
            "responsable",
            "miembro",
            "tipologia",
            "es_pilot",
            "url",
        )
        extra_kwargs = {
            "zone": {"write_only": True},
        }


class VisitAnimalPathSerializer(BasePathSerializer):
    fecha_visita = serializers.StringRelatedField(many=False, source="visited_at")
    especialista = serializers.StringRelatedField(source="employ_specialist")
    responsable = serializers.StringRelatedField(source="employ_responsable")
    actividad = serializers.StringRelatedField(many=False, source="activity")
    enfermedad_observación = serializers.StringRelatedField(
        source="sickness_observation"
    )
    diagnostico = serializers.StringRelatedField(many=False, source="diagnostic")

    @staticmethod
    def get_path():
        return "visits-animals"

    class Meta:
        model = VisitAnimal
        fields = [
            "fecha_visita",
            "especialista",
            "responsable",
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


class VisitGrassPathSerializer(BasePathSerializer):
    fecha_visita = serializers.StringRelatedField(source="visited_at")
    especialista = serializers.StringRelatedField(source="employ_specialist")
    responsable = serializers.StringRelatedField(source="employ_responsable")
    actividad = serializers.StringRelatedField(source="activity")

    @staticmethod
    def get_path():
        return "visits-grass"

    class Meta:
        model = VisitGrass
        fields = [
            "fecha_visita",
            "especialista",
            "responsable",
            "actividad",
            "url",
        ]


class ProductionUnitDetailsPathSerializer(BasePathSerializer):
    zona_nombre = serializers.StringRelatedField(many=False, source="zone")
    comunidad = serializers.StringRelatedField(many=False, source="community")
    sector = serializers.StringRelatedField(many=False)
    responsable = serializers.StringRelatedField(
        many=False, source="person_responsable"
    )
    miembro = serializers.StringRelatedField(many=False, source="person_member")
    tipologia = serializers.StringRelatedField(many=False, source="tipology")
    es_pilot = serializers.StringRelatedField(many=False, source="is_pilot")
    visitas_animales = serializers.SerializerMethodField()
    visitas_pastos = serializers.SerializerMethodField()

    @staticmethod
    def get_path():
        return "production_units"

    def get_visitas_animales(self, obj):
        data = VisitAnimal.objects.filter(production_unit__id=obj.id)
        serializer = VisitAnimalPathSerializer(instance=data, many=True)
        return serializer.data

    def get_visitas_pastos(self, obj):
        data = VisitGrass.objects.filter(production_unit__id=obj.id)
        serializer = VisitGrassPathSerializer(instance=data, many=True)
        return serializer.data

    class Meta:
        model = ProductionUnit
        fields = (
            "responsable",
            "miembro",
            "zona_nombre",
            "zone",
            "comunidad",
            "sector",
            "tipologia",
            "es_pilot",
            "url",
            "visitas_animales",
            "visitas_pastos",
        )
        extra_kwargs = {
            "zone": {"write_only": True},
        }


class ProductionUnitViewSet(viewsets.ModelViewSet):
    queryset = ProductionUnit.objects.all()
    serializer_class = ProductionUnitPathSerializer
    serializer_details_class = ProductionUnitDetailsPathSerializer
    filterset_fields = {
        "zone__name": ["contains"],
        "person_responsable__name": ["contains"],
    }

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = self.serializer_details_class
        return super().retrieve(request, *args, **kwargs)
