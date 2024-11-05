from rest_framework import viewsets, serializers
from django.db.models import F, Sum
from core.models import (
    ProductionUnit,
    VisitAnimalHealth,
    VisitGrass,
    VisitComponent2,
    VisitComponent3,
)
from .utils import BasePathSerializer


class ProductionUnitPathSerializer(BasePathSerializer):
    zona_nombre = serializers.StringRelatedField(many=False, source="zone")
    comunidad = serializers.StringRelatedField(many=False, source="community")
    sector_nombre = serializers.StringRelatedField(many=False, source="sector")
    responsable = serializers.StringRelatedField(
        many=False, source="person_responsable"
    )
    dni = serializers.StringRelatedField(many=False, source="person_responsable.dni")
    miembro = serializers.StringRelatedField(many=False, source="person_member")
    tipologia = serializers.StringRelatedField(many=False, source="tipology")

    @staticmethod
    def get_path():
        return "production_units"

    class Meta:
        model = ProductionUnit
        fields = (
            "id",
            "zone",
            "community",
            "sector",
            "person_responsable",
            "zona_nombre",
            "comunidad",
            "sector_nombre",
            "responsable",
            "dni",
            "miembro",
            "tipologia",
            "url",
        )
        extra_kwargs = {
            # "zone": {"write_only": True},
            # "community": {"write_only": True},
            # "sector": {"write_only": True},
            # "person_responsable": {"write_only": True},
        }


class VisitAnimalHealthPathSerializer(BasePathSerializer):
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
        model = VisitAnimalHealth
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
    # has = serializers.StringRelatedField(source="planting_intention_hectares")

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


class VisitComponent2PathSerializer(BasePathSerializer):
    fecha_visita = serializers.StringRelatedField(source="visited_at")
    especialista = serializers.StringRelatedField(source="employ_specialist")
    responsable = serializers.StringRelatedField(source="employ_responsable")
    actividad = serializers.StringRelatedField(source="activity")

    @staticmethod
    def get_path():
        return "visits-component-2"

    class Meta:
        model = VisitGrass
        fields = [
            "fecha_visita",
            "especialista",
            "responsable",
            "actividad",
            "url",
        ]


class VisitComponent3PathSerializer(BasePathSerializer):
    fecha_visita = serializers.StringRelatedField(source="visited_at")
    especialista = serializers.StringRelatedField(source="employ_specialist")
    responsable = serializers.StringRelatedField(source="employ_responsable")
    actividad = serializers.StringRelatedField(source="activity")

    @staticmethod
    def get_path():
        return "visits-component-3"

    class Meta:
        model = VisitGrass
        fields = [
            "fecha_visita",
            "especialista",
            "responsable",
            "actividad",
            "url",
        ]


class SumaPastosPathSerializer(serializers.Serializer):
    has_intens_siembra = serializers.DecimalField(decimal_places=2, max_digits=5)
    anal_suelo = serializers.IntegerField()
    horas_arado = serializers.IntegerField()
    horas_rastra = serializers.IntegerField()
    kg_avena = serializers.IntegerField()
    kg_vicia = serializers.IntegerField()
    kg_alfalfa = serializers.IntegerField()
    kg_dacylis = serializers.IntegerField()
    kg_ryegrass = serializers.IntegerField()
    kg_trebol = serializers.IntegerField()
    fertilizante = serializers.IntegerField()
    has_siembra_avena = serializers.IntegerField()
    has_siembra_avena_vicia = serializers.IntegerField()
    has_siembra_alfalfa_dactylis = serializers.IntegerField()
    has_siembra_ryegrass_trebol = serializers.IntegerField()
    rendimiento_anual = serializers.IntegerField()
    asistencia_tecnica = serializers.IntegerField()
    capac_inst_perennes = serializers.IntegerField()
    capac_inst_anual = serializers.IntegerField()
    capac_manejo_conserv = serializers.IntegerField()


class SumaAnimalesPathSerializer(serializers.Serializer):
    total_vacas = serializers.IntegerField()
    total_vaquillonas = serializers.IntegerField()
    total_vaquillas = serializers.IntegerField()
    total_terrenos = serializers.IntegerField()
    total_toretes = serializers.IntegerField()
    total_toros = serializers.IntegerField()
    total_vacunos = serializers.IntegerField()
    total_ovinos = serializers.IntegerField()
    total_alpacas = serializers.IntegerField()
    total_llamas = serializers.IntegerField()
    total_canes = serializers.IntegerField()


class ProductionUnitDetailsPathSerializer(BasePathSerializer):
    zona_nombre = serializers.StringRelatedField(many=False, source="zone")
    comunidad_nombre = serializers.StringRelatedField(many=False, source="community")
    sector_nombre = serializers.StringRelatedField(many=False, source="sector")
    responsable = serializers.StringRelatedField(
        many=False, source="person_responsable"
    )
    dni = serializers.StringRelatedField(many=False, source="person_responsable.dni")
    miembro = serializers.StringRelatedField(many=False, source="person_member")
    tipologia = serializers.StringRelatedField(many=False, source="tipology")
    suma_animales = serializers.SerializerMethodField()
    suma_pastos = serializers.SerializerMethodField()
    visitas_animales = serializers.SerializerMethodField()
    visitas_pastos = serializers.SerializerMethodField()
    visitas_capacitaciones = serializers.SerializerMethodField()

    @staticmethod
    def get_path():
        return "production_units"

    def get_visitas_animales(self, obj):
        data = VisitAnimalHealth.objects.filter(production_unit__id=obj.id)
        serializer = VisitAnimalHealthPathSerializer(instance=data, many=True)
        return serializer.data

    def get_visitas_pastos(self, obj):
        data = VisitGrass.objects.filter(production_unit__id=obj.id)
        serializer = VisitGrassPathSerializer(instance=data, many=True)
        return serializer.data

    def get_visitas_componente_2(self, obj):
        data = VisitComponent2.objects.filter(production_unit__id=obj.id)
        serializer = VisitComponent2PathSerializer(instance=data, many=True)
        return serializer.data

    def get_visitas_componente_3(self, obj):
        data = VisitComponent3.objects.filter(production_unit__id=obj.id)
        serializer = VisitComponent3PathSerializer(instance=data, many=True)
        return serializer.data

    def get_suma_pastos(self, obj):
        data = VisitGrass.objects.filter(production_unit__id=obj.id).aggregate(
            has_intens_siembra=Sum("planting_intention_hectares", default=0),
            anal_suelo=Sum("ground_analysis", default=0),
            horas_arado=Sum("plow_hours", default=0),
            horas_rastra=Sum("dredge_hours", default=0),
            kg_avena=Sum("oat_kg", default=0),
            kg_vicia=Sum("vicia_kg", default=0),
            kg_alfalfa=Sum("alfalfa_kg", default=0),
            kg_dacylis=Sum("dactylis_kg", default=0),
            kg_ryegrass=Sum("ryegrass_kg", default=0),
            kg_trebol=Sum("trebol_b_kg", default=0),
            fertilizante=Sum("fertilizer", default=0),
            has_siembra_avena=Sum("avena_planted_hectares", default=0),
            has_siembra_avena_vicia=Sum("avena_vicia_planted_hectares", default=0),
            has_siembra_alfalfa_dactylis=Sum(
                "alfalfa_dactylis_planted_hectares", default=0
            ),
            has_siembra_ryegrass_trebol=Sum(
                "ryegrass_trebol_planted_hectares", default=0
            ),
            rendimiento_anual=Sum("anual_yield", default=0),
            asistencia_tecnica=Sum("technical_assistance", default=0),
            capac_inst_perennes=Sum("technical_training_perennial", default=0),
            capac_inst_anual=Sum("technical_training_anual", default=0),
            capac_manejo_conserv=Sum("technical_training_conservation", default=0),
        )
        serializer = SumaPastosPathSerializer(instance=data, many=False)
        return serializer.data

    def get_suma_animales(self, obj):
        data = VisitAnimalHealth.objects.filter(production_unit__id=obj.id).aggregate(
            total_vacas=Sum("vaca", default=0),
            total_vaquillonas=Sum("vaquillona", default=0),
            total_vaquillas=Sum("vaquilla", default=0),
            total_terrenos=Sum("terreno", default=0),
            total_toretes=Sum("torete", default=0),
            total_toros=Sum("toro", default=0),
            total_vacunos=Sum("vacunos", default=0),
            total_ovinos=Sum("ovinos", default=0),
            total_alpacas=Sum("alpacas", default=0),
            total_llamas=Sum("llamas", default=0),
            total_canes=Sum("canes", default=0),
        )
        serializer = SumaAnimalesPathSerializer(instance=data, many=False)
        return serializer.data

    class Meta:
        model = ProductionUnit
        fields = (
            "id",
            "zone",
            "community",
            "sector",
            "person_responsable",
            "responsable",
            "dni",
            "miembro",
            "zona_nombre",
            "comunidad_nombre",
            "sector_nombre",
            "tipologia",
            "url",
            "suma_animales",
            "suma_pastos",
            "visitas_animales",
            "visitas_pastos",
            "visitas_componente_2",
            "visitas_componente_3",
        )


#        extra_kwargs = {
#            "zone": {"write_only": True},
#            "community": {"write_only": True},
#        }


class ProductionUnitViewSet(viewsets.ModelViewSet):
    queryset = ProductionUnit.objects.filter(is_official=True)
    serializer_class = ProductionUnitPathSerializer
    serializer_details_class = ProductionUnitDetailsPathSerializer
    filterset_fields = {
        "person_responsable__name": ["icontains"],
        "person_responsable__dni": ["icontains"],
        "zone__name": ["icontains"],
        "community__name": ["icontains"],
        "sector__name": ["icontains"],
    }

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = self.serializer_details_class
        return super().retrieve(request, *args, **kwargs)
