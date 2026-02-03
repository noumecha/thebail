from rest_framework import serializers

class LocalisationSerializer(serializers.Serializer):
    """Serializer pour les données de localisation (pas un modèle séparé)"""
    pays_id = serializers.IntegerField(required=False, allow_null=True)
    ville = serializers.CharField(required=False, allow_blank=True)
    rue = serializers.CharField(required=False, allow_blank=True)
    region_id = serializers.IntegerField(required=False, allow_null=True)
    departement_id = serializers.IntegerField(required=False, allow_null=True)
    arrondissement_id = serializers.IntegerField(required=False, allow_null=True)
    quartier = serializers.CharField(required=False, allow_blank=True)
    coordonnees_gps = serializers.CharField(required=False, allow_blank=True)
