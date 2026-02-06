from rest_framework import serializers
from ..models import *
from .ImmeubleSerializer  import ImmeubleSerializer
from .ContratSerializer  import ContratSerializer
from .PieceCollecteSerializer import PieceCollecteSerializer
from django.core.files.base import ContentFile
import base64
import uuid
import json

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
        """Créer les pièces collectées avec leurs images"""
        for piece_data in pieces_data:
            # Extraire les images
            images_data = piece_data.pop('images', [])

            # Créer la pièce collectée
            piece_collecte = PieceCollectes.objects.create(
                Collecte=fiche,
                Piece_id=piece_data['Piece'],
                statut=piece_data['statut'],
                nombre=piece_data['nombre']
            )

            # ✅ Créer les images associées
            for index, image_data in enumerate(images_data):
                try:
                    # Décoder le base64
                    format, imgstr = image_data['content'].split(';base64,')
                    ext = format.split('/')[-1]

                    # Générer un nom de fichier unique
                    filename = f"{uuid.uuid4()}.{ext}"

                    # Créer le fichier
                    image_file = ContentFile(
                        base64.b64decode(imgstr),
                        name=filename
                    )

                    # Créer l'enregistrement image
                    ImagePieceCollecte.objects.create(
                        piece_collecte=piece_collecte,
                        image=image_file,
                        ordre=index + 1
                    )

                except Exception as e:
                    print(f"Erreur lors du traitement de l'image {index}: {str(e)}")
                    continue
