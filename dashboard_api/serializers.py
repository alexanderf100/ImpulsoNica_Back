from rest_framework import serializers
from .models import FactOfertaslaborales


class FactOfertaslaboralesSerializer(serializers.ModelSerializer):
    # Traemos nombres legibles desde las dimensiones
    sector_nombre = serializers.CharField(source='sectorkey.nombresector', read_only=True)
    empresa_nombre = serializers.CharField(source='empresakey.nombreempresa', read_only=True)
    ubicacion_depto = serializers.CharField(source='ubicacionkey.departamento', read_only=True)

    class Meta:
        model = FactOfertaslaborales
        fields = '__all__'