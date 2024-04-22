from rest_framework import viewsets, serializers
from django.db.models import F, Sum
from core.models import ProductionUnit, VisitAnimalHealth, VisitGrass, VisitComponents
from .utils import BasePathSerializer


class ProductionUnitPathSerializer(BasePathSerializer):
    zona_nombre = serializers.StringRelatedField(many=False, source="zone")
    comunidad = serializers.StringRelatedField(many=False, source="community")
    sector = serializers.StringRelatedField(many=False)
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
            "zona_nombre",
            "zone",
            "comunidad",
            "sector",
            "responsable",
            "dni",
            "miembro",
            "tipologia",
            "url",
        )
        extra_kwargs = {
            "zone": {"write_only": True},
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


class VisitComponentsPathSerializer(BasePathSerializer):
    fecha_visita = serializers.StringRelatedField(source="visited_at")
    especialista = serializers.StringRelatedField(source="employ_specialist")
    responsable = serializers.StringRelatedField(source="employ_responsable")
    actividad = serializers.StringRelatedField(source="activity")

    @staticmethod
    def get_path():
        return "visits-components"

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
    has_intens_siembra = serializers.IntegerField()
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
    comunidad = serializers.StringRelatedField(many=False, source="community")
    sector = serializers.StringRelatedField(many=False)
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

    def get_visitas_capacitaciones(self, obj):
        data = VisitComponents.objects.filter(production_unit__id=obj.id)
        serializer = VisitComponentsPathSerializer(instance=data, many=True)
        return serializer.data

    def get_suma_pastos(self, obj):
        data = (
            VisitGrass.objects.filter(production_unit__id=obj.id)
            .annotate(
                has_intens_siembra=Sum(F("planting_intention_hectares")),
                anal_suelo=Sum(F("ground_analysis")),
                horas_arado=Sum(F("plow_hours")),
                horas_rastra=Sum(F("dredge_hours")),
                kg_avena=Sum(F("oat_kg")),
                kg_vicia=Sum(F("vicia_kg")),
                kg_alfalfa=Sum(F("alfalfa_kg")),
                kg_dacylis=Sum(F("dactylis_kg")),
                kg_ryegrass=Sum(F("ryegrass_kg")),
                kg_trebol=Sum(F("trebol_b_kg")),
                fertilizante=Sum(F("fertilizer")),
                has_siembra_avena=Sum(F("avena_planted_hectares")),
                has_siembra_avena_vicia=Sum(F("avena_vicia_planted_hectares")),
                has_siembra_alfalfa_dactylis=Sum(
                    F("alfalfa_dactylis_planted_hectares")
                ),
                has_siembra_ryegrass_trebol=Sum(F("ryegrass_trebol_planted_hectares")),
                rendimiento_anual=Sum(F("anual_yield")),
                asistencia_tecnica=Sum(F("technical_assistance")),
                capac_inst_perennes=Sum(F("technical_training_perennial")),
                capac_inst_anual=Sum(F("technical_training_anual")),
                capac_manejo_conserv=Sum(F("technical_training_conservation")),
            )
            .values(
                "has_intens_siembra",
                "anal_suelo",
                "horas_arado",
                "horas_rastra",
                "kg_avena",
                "kg_vicia",
                "kg_alfalfa",
                "kg_dacylis",
                "kg_ryegrass",
                "kg_trebol",
                "fertilizante",
                "has_siembra_avena",
                "has_siembra_avena_vicia",
                "has_siembra_alfalfa_dactylis",
                "has_siembra_ryegrass_trebol",
                "rendimiento_anual",
                "asistencia_tecnica",
                "capac_inst_perennes",
                "capac_inst_anual",
                "capac_manejo_conserv",
            )
        )
        serializer = SumaPastosPathSerializer(instance=data, many=True)
        return serializer.data

    def get_suma_animales(self, obj):
        #         data = (
        #            VisitGrass.objects.filter(production_unit__id=obj.id)
        #            .annotate(
        #                has_intens_siembra=Sum(F("planting_intention_hectares")),
        #                anal_suelo=Sum(F("ground_analysis")),
        #                horas_arado=Sum(F("plow_hours")),
        #

        data2 = VisitAnimalHealth.objects.filter(production_unit__id=obj.id).annotate(
            total_vacas=Sum(F("vaca"), default=0),
            total_vaquillonas=Sum(F("vaquillona"), default=0),
            total_vaquillas=Sum(F("vaquilla"), default=0),
            total_terrenos=Sum(F("terreno"), default=0),
            total_toretes=Sum(F("torete"), default=0),
            total_toros=Sum(F("toro"), default=0),
            total_vacunos=Sum(F("vacunos"), default=0),
            total_ovinos=Sum(F("ovinos"), default=0),
            total_alpacas=Sum(F("alpacas"), default=0),
            total_llamas=Sum(F("llamas"), default=0),
            total_canes=Sum(F("canes"), default=0),
        )

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
            "responsable",
            "dni",
            "miembro",
            "zona_nombre",
            "zone",
            "comunidad",
            "sector",
            "tipologia",
            "url",
            "suma_animales",
            "suma_pastos",
            "visitas_animales",
            "visitas_pastos",
            "visitas_capacitaciones",
        )
        extra_kwargs = {
            "zone": {"write_only": True},
        }


class ProductionUnitViewSet(viewsets.ModelViewSet):
    queryset = ProductionUnit.objects.filter(is_official=True)
    serializer_class = ProductionUnitPathSerializer
    serializer_details_class = ProductionUnitDetailsPathSerializer
    filterset_fields = {
        "zone__name": ["contains"],
        "person_responsable__name": ["contains"],
    }

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = self.serializer_details_class
        return super().retrieve(request, *args, **kwargs)
