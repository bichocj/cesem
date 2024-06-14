from core.models import VisitGeneticImprovementAlpaca
from rest_framework import serializers, viewsets

from .utils import BasePathSerializer
from .zones import ZonePathSerializer


class VisitGeneticImprovementAlpacaPathSerializer(BasePathSerializer):
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
        return "visits-alpaca"

    class Meta:
        model = VisitGeneticImprovementAlpaca
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
            "hato_number",
            "hato_babies_number",
            "hato_mothers_number",
            "hato_males_number",
            "female_alpaca_earring_number",
            "female_alpaca_race",
            "female_alpaca_color",
            "female_alpaca_age",
            "female_alpaca_category",
            "female_alpaca_total_score",
            "selected_alpacas_number",
            "empadre_date",
            "alpacas_empadradas",
            "alpacas_empadradas_number",
            "male_empadre_number",
            "second_service_date",
            "second_service_male_number",
            "pregnant",
            "empty",
            "baby_birthday",
            "baby_earring_number",
            "female_baby",
            "male_baby",
            "mortality_baby",
            "mother_of_baby",
            "father_of_baby",
            "training_male_attendance",
            "training_female_attendance",
            "technical_assistance_attendance",
            "url",
        ]        

class VisitGeneticImprovementAlpacaViewSet(viewsets.ModelViewSet):
    queryset = (
        VisitGeneticImprovementAlpaca.objects.select_related("production_unit")
        .select_related("production_unit__zone")
        .select_related("production_unit__person_responsable")        
        .select_related("employ_specialist", "employ_responsable")
        .select_related("activity")
        .all()
    )
    serializer_class = VisitGeneticImprovementAlpacaPathSerializer

    filterset_fields = {
        "production_unit__zone__name": ["icontains"],
        "production_unit__person_responsable__name": ["icontains"],
        "up_member_name": ["icontains"],
        "employ_specialist__name": ["icontains"],
        "employ_responsable__name": ["icontains"],
        "activity__name": ["icontains"],
    }
