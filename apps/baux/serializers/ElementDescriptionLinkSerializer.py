from rest_framework import serializers
from ..models import *

class ElementDescriptionLinkSerializer(serializers.Serializer):
    """Serializer pour la table intermédiaire Immeuble-ElementDescription"""
    element_id = serializers.IntegerField()
    statut = serializers.BooleanField()
    nombre = serializers.IntegerField(default=0)
