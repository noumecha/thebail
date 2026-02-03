from rest_framework import serializers
from ..models import *
from .ImmeubleSerializer  import ImmeubleSerializer
from .ContratSerializer  import ContratSerializer
from .PieceCollecteSerializer import PieceCollecteSerializer

class FicheCollecteSerializer(serializers.ModelSerializer):
    immeuble = ImmeubleSerializer()
    contrat = ContratSerializer()
    pieces_collectees = PieceCollecteSerializer(many=True, required=False)

    class Meta:
        model = Collectes
        fields = '__all__'

    def create(self, validated_data):
        """Création avec gestion des relations imbriquées"""
        # Extraire les données imbriquées
        immeuble_data = validated_data.pop('immeuble')
        contrat_data = validated_data.pop('contrat')
        pieces_data = validated_data.pop('pieces_collectees', [])

        # Créer l'immeuble
        immeuble_serializer = ImmeubleSerializer()
        immeuble = immeuble_serializer.create(immeuble_data)

        # Créer le contrat
        contrat_serializer = ContratSerializer()
        contrat = contrat_serializer.create(contrat_data)

        # Créer la fiche de collecte
        fiche = Collectes.objects.create(
            Immeuble=immeuble,
            Contrat=contrat,
            **validated_data
        )

        # Créer les pièces collectées
        self._create_pieces_collectees(pieces_data, fiche)

        return fiche

    # Créer les pièces collectées
    def _create_pieces_collectees(self, pieces_data, fiche):
        """Créer les pièces collectées"""
        for piece_data in pieces_data:
            PieceCollectes.objects.create(
                fiche_collecte=fiche,
                piece_id=piece_data['piece_id'],
                statut=piece_data['statut'],
                nombre=piece_data['nombre']
            )
