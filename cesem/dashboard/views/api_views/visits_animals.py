from core.models import VisitAnimalHealth, ProductionUnit
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
    actividad = serializers.StringRelatedField(many=False, source="activity")
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
            "zona",
            "comunidad",
            "sector",
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


class UpSerializer(serializers.Serializer):
    zona = serializers.StringRelatedField(many=False, source="production_unit.zone")
    comunidad = serializers.StringRelatedField(
        many=False, source="production_unit.community"
    )
    sector = serializers.StringRelatedField(many=False, source="production_unit.sector")
    up_responsable = serializers.StringRelatedField(
        many=False, source="production_unit.person_responsable"
    )    
     

class VisitAnimalHealthDetailsPathSerializer(BasePathSerializer):

    up_miembro = serializers.StringRelatedField(many=False, source="up_member")
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
            'production_unit',
            "visited_at",
            'up',
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
        .all()
    )
    serializer_class = VisitAnimalHealthPathSerializer
    serializer_details_class = VisitAnimalHealthDetailsPathSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = self.serializer_details_class
        return super().retrieve(request, *args, **kwargs)
    
    # def update(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        # kwargs['partial'c] = True
        # print(request.data)
    #    print('request.data.get(production_unit)', request.data.get('production_unit'))
    #    kwargs['production_unit'] = request.data.get('production_unit')
    #    return super().update(request, *args, **kwargs)
    
    def perform_update(self, serializer):
        # import pdb; pdb.set_trace()
        instance = self.get_object()  # instance before update
        production_unit_id = self.request.data.get("production_unit", None)  # read data from request
        production_unit = ProductionUnit.objects.get(id=production_unit_id)
        if self.request.user.is_authenticated:
            updated_instance = serializer.save(production_unit=production_unit)
        else:
            updated_instance = serializer.save()


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
