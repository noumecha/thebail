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
    # ✅ Utiliser source pour mapper les noms de champs
    immeuble = ImmeubleSerializer(source='Immeuble', required=False)
    contrat = ContratSerializer(source='Contrat', required=False)
    pieces_collectees = PieceCollecteSerializer(many=True, required=False)

    class Meta:
        model = Collectes
        fields = '__all__'

    def create(self, validated_data):
        """Création avec gestion des relations imbriquées"""
        print("📥 Données reçues:")
        print(validated_data)
        # Extraire les données imbriquées
        immeuble_data = validated_data.pop('Immeuble')
        contrat_data = validated_data.pop('Contrat')
        pieces_data = validated_data.pop('pieces_collectees', [])

        # Créer l'immeuble
        immeuble_serializer = ImmeubleSerializer()
        immeuble = immeuble_serializer.create(immeuble_data)

        # Créer le contrat
        contrat_serializer = ContratSerializer()
        contrat = contrat_serializer.create(contrat_data)

        # liaison avec le responsable de collecte
        matricule_agent = self.initial_data.get('agent_collecte_id')
        agent = AgentCollecte.objects.get(Matricule=matricule_agent) if matricule_agent else None

        # Créer la fiche de collecte
        fiche = Collectes.objects.create(
            Immeuble=immeuble,
            Contrat=contrat,
            Agent=agent,
            **validated_data
        )

        # Créer les pièces collectées
        self._create_pieces_collectees(pieces_data, fiche)

        return fiche

    def update(self, instance, validated_data):
        """Mise à jour avec gestion des relations imbriquées"""
        print("📥 Données reçues pour update:")
        print(json.dumps(self.initial_data, indent=2, ensure_ascii=False))

        # Extraire les données imbriquées
        immeuble_data = validated_data.pop('Immeuble', None)  # ✅ Utiliser 'Immeuble' pas 'immeuble'
        contrat_data = validated_data.pop('Contrat', None)    # ✅ Utiliser 'Contrat' pas 'contrat'
        pieces_data = validated_data.pop('pieces_collectees', None)

        # Mettre à jour l'agent
        agent_id = self.initial_data.get('agent_collecte_id')
        if agent_id:
            agent = AgentCollecte.objects.get(id=agent_id)
            instance.Agent = agent

        # Mettre à jour les champs simples de la fiche
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # ✅ Mettre à jour l'immeuble (passer l'instance existante)
        if immeuble_data:
            immeuble_serializer = ImmeubleSerializer()
            if instance.Immeuble:
                immeuble_serializer.update(instance.Immeuble, immeuble_data)
            else:
                instance.Immeuble = immeuble_serializer.create(immeuble_data)
                instance.save()

        # ✅ Mettre à jour le contrat (passer l'instance existante)
        if contrat_data:
            contrat_serializer = ContratSerializer()
            if instance.Contrat:
                contrat_serializer.update(instance.Contrat, contrat_data)
            else:
                instance.Contrat = contrat_serializer.create(contrat_data)
                instance.save()

        # Mettre à jour les pièces collectées
        if pieces_data is not None:
            # ✅ Ne pas supprimer, utiliser update_or_create
            self._update_pieces_collectees(pieces_data, instance)

        return instance

    def to_representation(self, instance):
        """Personnaliser la représentation pour l'affichage"""
        # ✅ Ne pas appeler super() qui essaie d'accéder à 'immeuble'
        # Construire la représentation manuellement
        representation = {
            'id': instance.id,
            'Numero_fiche_de_collecte': instance.Numero_fiche_de_collecte,
            'Date_de_collecte': instance.Date_de_collecte,
            'observation_generale': instance.observation_generale,
            'signature_responsable': instance.signature_responsable,
            'agent_collecte_id': instance.Agent_id,
            'matricule_agent': instance.Agent.Matricule if instance.Agent else None,
        }

        # ✅ Ajouter les informations de l'agent
        if instance.Agent:
            representation['Agent'] = {
                'id': instance.Agent.id,
                'nom': instance.Agent.Nom,
                'prenom': instance.Agent.Prenom,
                'matricule': instance.Agent.Matricule
            }

        # ✅ Ajouter l'immeuble avec toutes ses relations
        if instance.Immeuble:
            immeuble = instance.Immeuble
            pays = Pays.objects.get(id=immeuble.pays_id).LibelleFR if immeuble.pays_id else None,
            region = Regions.objects.get(id=immeuble.region_id).Libelle if immeuble.region_id else None,
            departement = Departements.objects.get(id=immeuble.departement_id).LibelleFR if immeuble.departement_id else None,
            arrondissement = Arrondissemements.objects.get(id=immeuble.arrondissement_id).LibelleFR if immeuble.arrondissement_id else None,
            immeuble_data = {
                'id': immeuble.id,
                'Designation': immeuble.Designation,
                'type_construction_id': immeuble.Construction_id,
                'type_location_id': immeuble.Type_location_id,
                'Date_Construction': immeuble.Date_Construction,
                'Nombre_de_pieces': str(immeuble.Nombre_de_pieces) if immeuble.Nombre_de_pieces else None,
                'Superficie_louer': str(immeuble.Superficie_louer) if immeuble.Superficie_louer else None,
                'statut_batisse_id': immeuble.Situation_batisse_id,
                'revetement_int_id': immeuble.Revetement_interieure_id,
                'revetement_ext_id': immeuble.Revetement_exterieure_id,
                'observation': immeuble.observation,
                'pays_id': immeuble.pays_id,
                'pays': {
                    'id': immeuble.pays_id,
                    'libelle': pays
                },
                'ville': immeuble.Ville,
                'rue': immeuble.Rue,
                'region_id': immeuble.region_id,
                'region': {
                    'id': immeuble.region_id,
                    'libelle': region
                },
                'departement_id': immeuble.departement_id,
                'departement': {
                    'id': immeuble.departement_id,
                    'libelle': departement
                },
                'arrondissement_id': immeuble.arrondissement_id,
                'arrondissement': {
                    'id': immeuble.arrondissement_id,
                    'libelle': arrondissement
                },
                'quartier': immeuble.Quartier,
                'coordonnees_gps': immeuble.Coordonee_gps,
                'elements_description': [],
                'occupants_residents': [],
                'occupants_bureaux': []
            }

            # Éléments de description
            elements = ImmeubleElement.objects.filter(immeuble=immeuble)
            immeuble_data['elements_description'] = [
                {
                    'element_id': el.element_id,
                    'statut': el.statut,
                    'nombre': el.nombre
                }
                for el in elements
            ]

            # Occupants résidents
            occupants_res = Occupants.objects.filter(Immeuble=immeuble)
            immeuble_data['occupants_residents'] = [
                {
                    'nom_prenom': occ.Nom_Prenom_occupant_residence,
                    'administration': occ.Administration_rattachement.id if occ.Administration_rattachement else None,
                    'administration_rattachement': {
                        'id': occ.Administration_rattachement.id if occ.Administration_rattachement else None,
                        'libelle': occ.Administration_rattachement.LibelleFr if occ.Administration_rattachement else None
                    },
                    'fonction': occ.Fonction_occupant_residence,
                    'matricule': occ.Matricule_occupant_residence,
                    'ref_acte': occ.Ref_ActeJuridique_attribution,
                    'date_signature': occ.Date_Signature_acte_juridique
                }
                for occ in occupants_res
            ]

            # Occupants bureaux
            occupants_bur = OccupantBureaux.objects.filter(Immeuble=immeuble)
            immeuble_data['occupants_bureaux'] = [
                {
                    'service': occ.Service_occupant_bureau.id if occ.Service_occupant_bureau else None,
                    'service_occupant_bureau' : {
                        'id': occ.Service_occupant_bureau.id if occ.Service_occupant_bureau else None,
                        'libelle': occ.Service_occupant_bureau.LibelleFr if occ.Service_occupant_bureau else None
                    },
                    'administration': occ.Administration_correspondante.id if occ.Administration_correspondante else None,
                    'administration_correspondante': {
                        'id': occ.Administration_correspondante.id if occ.Administration_correspondante else None,
                        'libelle': occ.Administration_correspondante.LibelleFr if occ.Administration_correspondante else None
                    },
                    'fonction_responsable': occ.Fonction_occupant_bureau,
                    'ref_acte': occ.Ref_ActeJuridique_attribution,
                    'date_signature': occ.Date_signature_acte_attribution
                }
                for occ in occupants_bur
            ]

            representation['immeuble'] = immeuble_data

        # ✅ Ajouter le contrat avec toutes ses relations
        if instance.Contrat:
            contrat = instance.Contrat
            contrat_data = {
                'id': contrat.id,
                'TypeContrat': contrat.TypeContrat_id,
                'Numero_contrat': contrat.Numero_contrat,
                'Date_Signature_contrat': contrat.Date_Signature_contrat,
                'Fonction_signataire_contrat': contrat.Fonction_signataire_contrat,
                'Date_effet_contrat': contrat.Date_effet_contrat,
                'Existence_visa_budgétaire': contrat.Existence_visa_budgétaire,
                'Duree_Contrat': contrat.Duree_Contrat,
                'Tacite_reconduction_contrat': contrat.Tacite_reconduction_contrat,
                'Regime_fiscal_contrat': contrat.Regime_fiscal_contrat,
                'Montant_loyer_mensuel': str(contrat.Montant_loyer_mensuel) if contrat.Montant_loyer_mensuel else None,
                'Devise': contrat.Devise,
                'Periodicite_Reglement_id': contrat.Periodicite_Reglement_id,
                'Existence_avenant': contrat.Existence_avenant,
                'bailleur': None,
                'avenants': [],
                'non_mandatements': []
            }

            # Bailleur
            if contrat.Bailleur:
                bailleur = contrat.Bailleur
                contrat_data['bailleur'] = {
                    'id': bailleur.id,
                    'Type_personne': bailleur.Type_personne,
                    'Raison_social': bailleur.Raison_social,
                    'Nom_Prenom_Representant': bailleur.Nom_Prenom_Representant,
                    'Domicille_siege_social_bailleur': bailleur.Domicille_siege_social_bailleur,
                    'NIU': bailleur.NIU,
                    'Telephone': bailleur.Telephone,
                    'Num_doc': bailleur.Num_doc,
                    'Date_delivrance_doc': bailleur.Date_delivrance_doc,
                    'Statut_bailleur': bailleur.Statut_bailleur,
                    'Banque': bailleur.Banque,
                    'RIB': bailleur.RIB,
                    'Intitule_compte': bailleur.Intitule_compte,
                    'ayants_droit': []
                }

                # Ayants droit
                ayants = Ayant_droits.objects.filter(Bailleur=bailleur)
                contrat_data['bailleur']['ayants_droit'] = [
                    {
                        'Nom_Prenom': ayant.Nom_Prenom_ayant_droit,
                        'Contact': ayant.Contact_ayant_droit,
                        'Ref_Grosse': ayant.Reference_Grosse_ayant_droit,
                        'Date_delivrance_Grosse': ayant.Date_delivrance_grosse,
                        'Ref_Certificat_non_appel': ayant.Reference_certificat_non_appel,
                        'Date_delivrance_Certificat': ayant.Date_delivrance_certificat_non_appel
                    }
                    for ayant in ayants
                ]

            # Avenants
            avenants = Avenants.objects.filter(contrat=contrat)
            contrat_data['avenants'] = [
                {
                    'Ref_Avenant': av.Ref_Avenant,
                    'Date_Signature': av.Date_Signature,
                    'Date_effet': av.Date_effet,
                    'Ancien_bailleur': av.Ancien_bailleur_id,
                    'Ancien_bailleur_object': {
                        'id': av.Ancien_bailleur_id,
                        'libelle': av.Ancien_bailleur.Raison_social if av.Ancien_bailleur else None
                    },
                    'Nouveau_bailleur': av.Nouveau_bailleur_id,
                    'Nouveau_bailleur_object': {
                        'id': av.Nouveau_bailleur_id,
                        'libelle': av.Nouveau_bailleur.Raison_social if av.Nouveau_bailleur else None
                    },
                    'Montant_TTC_Mensuel_ancien': str(av.Montant_TTC_Mensuel_ancien) if av.Montant_TTC_Mensuel_ancien else None,
                    'Montant_TTC_Mensuel_Nouveau': str(av.Montant_TTC_Mensuel_Nouveau) if av.Montant_TTC_Mensuel_Nouveau else None
                }
                for av in avenants
            ]

            # Non-mandatements
            non_mandatements = Non_Mandatement.objects.filter(Contrat=contrat)
            contrat_data['non_mandatements'] = [
                {
                    'Exercice': {'id': nm.Exercice_id, 'libelle': nm.Exercice.LibelleFR if nm.Exercice else None},
                    'Loyer_Mensuel': str(nm.Loyer_Mensuel) if nm.Loyer_Mensuel else None,
                    'Ref_Attestattion': nm.Ref_Attestattion,
                    'Date_signature': nm.Date_signature,
                    'janvier': nm.janvier,
                    'fevrier': nm.fevrier,
                    'mars': nm.mars,
                    'avril': nm.avril,
                    'mai': nm.mai,
                    'juin': nm.juin,
                    'juillet': nm.juillet,
                    'aout': nm.aout,
                    'septembre': nm.septembre,
                    'octobre': nm.octobre,
                    'novembre': nm.novembre,
                    'decembre': nm.decembre,
                    'Montant_total_exercice': str(nm.Montant_total_exercice) if nm.Montant_total_exercice else None,
                    'Visa_budgétaire': nm.Visa_budgétaire,
                    'Ref_contrat_avenant': nm.Ref_contrat_avenant
                }
                for nm in non_mandatements
            ]

            representation['contrat'] = contrat_data

        # ✅ Ajouter les pièces collectées avec images
        pieces = PieceCollectes.objects.filter(Collecte=instance).prefetch_related('images')
        representation['pieces_collectees'] = [
            {
                'piece_id': piece.Piece_id,
                'statut': piece.statut,
                'nombre': piece.nombre,
                'images': [
                    {
                        'id': img.id,
                        'image': img.image.url if img.image else None,
                        'legende': img.legende,
                        'ordre': img.ordre
                    }
                    for img in piece.images.all()
                ]
            }
            for piece in pieces
        ]

        return representation

    # Créer les pièces collectées
    def _create_pieces_collectees(self, pieces_data, fiche):
        #Créer les pièces collectées avec leurs images
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

    def _update_pieces_collectees(self, pieces_data, fiche):
        """Mettre à jour les pièces collectées sans supprimer les existantes"""
        existing_piece_ids = []

        for piece_data in pieces_data:
            images_data = piece_data.pop('images', [])
            piece_id = piece_data['Piece']

            # ✅ Mettre à jour ou créer la pièce
            piece_collecte, created = PieceCollectes.objects.update_or_create(
                Collecte=fiche,
                Piece_id=piece_id,
                defaults={
                    'statut': piece_data['statut'],
                    'nombre': piece_data['nombre']
                }
            )

            existing_piece_ids.append(piece_id)

            # ✅ Traiter les images
            ordre = 1
            for image_data in images_data:
                if image_data.get('existing'):
                    try:
                        existing_image = ImagePieceCollecte.objects.get(
                            id=image_data['id'],
                            piece_collecte=piece_collecte
                        )
                        existing_image.ordre = ordre
                        existing_image.save()
                        ordre += 1
                    except ImagePieceCollecte.DoesNotExist:
                        print(f"Image existante {image_data['id']} non trouvée")
                    continue

                # Créer nouvelle image
                try:
                    format, imgstr = image_data['content'].split(';base64,')
                    ext = format.split('/')[-1]
                    filename = f"{uuid.uuid4()}.{ext}"

                    image_file = ContentFile(
                        base64.b64decode(imgstr),
                        name=filename
                    )

                    ImagePieceCollecte.objects.create(
                        piece_collecte=piece_collecte,
                        image=image_file,
                        ordre=ordre
                    )
                    ordre += 1
                except Exception as e:
                    print(f"Erreur lors du traitement de l'image: {str(e)}")
                    continue

        # ✅ Supprimer les pièces qui ne sont plus cochées
        PieceCollectes.objects.filter(
            Collecte=fiche
        ).exclude(
            Piece_id__in=existing_piece_ids
        ).delete()
