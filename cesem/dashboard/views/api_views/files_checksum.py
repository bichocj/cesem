from rest_framework import viewsets, serializers, mixins
from core import models
from .utils import BasePathSerializer


class FilesChecksumPathSerializer(BasePathSerializer):
    fecha_importacion = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M", source="created_at"
    )
    visitas = serializers.StringRelatedField(many=False, source="visits")

    @staticmethod
    def get_path():
        return "files-checksum"

    class Meta:
        model = models.FilesChecksum
        fields = ("fecha_importacion", "filename", "visitas", "checksum", "url")
        extra_kwargs = {
            "zone": {"write_only": True},
        }


class FilesChecksumViewSet(viewsets.ReadOnlyModelViewSet, mixins.DestroyModelMixin,):
    queryset = models.FilesChecksum.objects.all()
    serializer_class = FilesChecksumPathSerializer

    def perform_destroy(self, instance):
        checksum = instance.checksum
        models.VisitGrass.objects.filter(checksum=checksum).delete()
        models.VisitAnimalHealth.objects.filter(checksum=checksum).delete()
        models.VisitGeneticImprovementVacuno.objects.filter(checksum=checksum).delete()
        models.VisitGeneticImprovementOvino.objects.filter(checksum=checksum).delete()
        models.VisitGeneticImprovementAlpaca.objects.filter(checksum=checksum).delete()
        instance.delete()
        