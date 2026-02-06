from rest_framework import serializers
from ..models import *

class ImagePieceCollecteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePieceCollecte
        fields = ['image', 'legende', 'ordre']

class PieceCollecteSerializer(serializers.ModelSerializer):
    piece_id = serializers.IntegerField(source='Piece')
    images = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = PieceCollectes
        fields = ['piece_id', 'statut', 'nombre', 'images']
