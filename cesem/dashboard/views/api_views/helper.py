from rest_framework import serializers

class UpSerializer(serializers.Serializer):
    zona = serializers.StringRelatedField(many=False, source="production_unit.zone")
    comunidad = serializers.StringRelatedField(
        many=False, source="production_unit.community"
    )
    sector = serializers.StringRelatedField(many=False, source="production_unit.sector")
    up_responsable = serializers.StringRelatedField(
        many=False, source="production_unit.person_responsable"
    )