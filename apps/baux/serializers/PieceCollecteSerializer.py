from rest_framework import serializers
from ..models import *
import json

class PieceCollecteSerializer(serializers.Serializer):
    """Pour la table intermédiaire FicheCollecte-Piece"""
    piece_id = serializers.IntegerField()
    statut = serializers.BooleanField()
    nombre = serializers.IntegerField(default=0)

    class Meta:
        model = PieceCollectes
        fields = '__all__'
