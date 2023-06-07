from rest_framework import viewsets

from core.models import Person
from .utils import BasePathSerializer


class PersonPathSerializer(BasePathSerializer):
    @staticmethod
    def get_path():
        return "people"

    class Meta:
        model = Person
        fields = ["name", "last_name", "dni", "url"]


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonPathSerializer
    filterset_fields = {
        "name": ["contains"],
        "last_name": ["contains"],
        "dni": ["contains"],
    }
