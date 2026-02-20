# Dans votre views.py
from django.http import JsonResponse
from django.db.models import Q
from django.views import View
from ..models import *
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializers import FicheCollecteSerializer
from django.db import transaction
import logging
import json

class Select2SearchView(View):
    """
    Classe générique pour les recherches Select2

    Utilisation :
    class MyCustomSearch(Select2SearchView):
        model = MyModel
        search_fields = ['field1', 'field2']
        result_fields = {'id': 'id', 'text': 'name'}
    """
    model = None
    search_fields = []
    page_size = 30
    order_by = None

    # Format Select2
    id_field = None
    text_template = None
    extra_fields = []
    show_all_when_empty = False

    def get_queryset(self, search_term):
        if not search_term and self.show_all_when_empty:
            return self.model.objects.all()

        q = Q()
        for field in self.search_fields:
            q |= Q(**{f"{field}__icontains": search_term})
        return self.model.objects.filter(q)

    def format_result(self, obj):
        text = self.text_template.format(**obj.__dict__)
        result = {
            "id": getattr(obj, self.id_field),
            "text": text
        }

        for field in self.extra_fields:
            result[field.lower()] = getattr(obj, field)

        return result

    def get(self, request):
        search_term = request.GET.get("q", "")
        page = int(request.GET.get("page", 1))

        qs = self.get_queryset(search_term)

        if self.order_by:
            qs = qs.order_by(self.order_by)

        start = (page - 1) * self.page_size
        end = start + self.page_size
        total = qs.count()

        objects = qs[start:end]

        return JsonResponse({
            "results": [self.format_result(obj) for obj in objects],
            "pagination": {"more": end < total}
        })

class AgentMatriculeSelect2(Select2SearchView):
    model = AgentCollecte
    search_fields = ["Matricule"]
    id_field = "Matricule"
    text_template = "{Matricule}"
    order_by = "Matricule"

class AgentNomSelect2(Select2SearchView):
    model = AgentCollecte
    search_fields = ["Matricule", "Nom", "Prenom"]
    id_field = "Matricule"
    text_template = "{Nom} {Prenom}"
    extra_fields = ["Matricule"]
    order_by = "Matricule"

class PaysSelect2(Select2SearchView):
    model = Pays
    search_fields = ["LibelleFR", "AbreviationFr"]
    id_field = "pk"
    text_template = "{LibelleFR} ({AbreviationFr})"
    extra_fields = []
    order_by = "LibelleFR"

class RegionSelect2(Select2SearchView):
    model = Regions
    search_fields = ["Libelle","code","AbreviationFr"]
    id_field = "pk"
    text_template = "{Libelle} ({AbreviationFr})"
    extra_fields = []
    order_by = "Libelle"

class DepartementSelect2(Select2SearchView):
    model = Departements
    search_fields = ["LibelleFR","AbreviationFr","code"]
    id_field = "pk"
    text_template = "{LibelleFR} ({AbreviationFr})"
    extra_fields = []
    order_by = "LibelleFR"

class ArrondissemntSelect2(Select2SearchView):
    model = Arrondissemements
    search_fields = ["LibelleFR","code","AbreviationFr"]
    id_field = "pk"
    text_template = "{LibelleFR} ({AbreviationFr})"
    extra_fields = []
    order_by = "LibelleFR"

class AdminisrationsSelect2(Select2SearchView):
    model = Administrations
    search_fields = ["LibelleFr","AbreviationFr","code"]
    id_field = "pk"
    text_template = "{code} - {LibelleFr}"
    extra_fields = []
    order_by = "LibelleFr"

class StructuresSelect2(Select2SearchView):
    model = Structures
    search_fields = ["LibelleFr","CodeFr"]
    id_field = "pk"
    text_template = "{LibelleFr}"
    extra_fields = []
    order_by = "LibelleFr"

class BailleursSelect2(Select2SearchView):
    model = Bailleurs
    search_fields = ["Nom_prenom","Raison_social","NIU","Maticule","Nom_Prenom_Representant"]
    id_field = "pk"
    text_template = "{Nom_prenom} {Raison_social}"
    extra_fields = []
    order_by = "Nom_prenom"

class ExercicesSelect2(Select2SearchView):
    model = Exercice
    search_fields = ["annee", "LibelleFR"]
    id_field = "pk"
    text_template = "Exercice budgetaire {annee}"
    extra_fields = ["annee"]
    order_by = "-annee"
    show_all_when_empty = True

class BanquesSelect2(Select2SearchView):
    model = Banques
    search_fields = ["codeBanque","sigle","denominationFR","denominationUS","denominationES","siege","adresse","telephone","fax","email"]
    id_field = "pk"
    text_template = "{codeBanque} - {sigle}"
    extra_fields = []
    order_by = "sigle"

def get_agent_name(request):
    """API pour récupérer le nom complet d'un agent par matricule"""
    if request.method == 'GET':
        matricule_agent = request.GET.get('matricule_agent')
        if not matricule_agent:
            return JsonResponse({'error': 'Aucun agent sélectionné'}, status=400)
        try:
            agent = AgentCollecte.objects.get(Matricule=matricule_agent)
            name = f"{agent.Nom} {agent.Prenom}"
            return JsonResponse({'agent': name, 'success': True}, status=200)
        except AgentCollecte.DoesNotExist:
            return JsonResponse({'error': 'Agent non trouvé', 'success': False}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'Erreur lors de la récupération de l\'agent', 'success': False}, status=500)
    return JsonResponse({'error': 'Requête invalide', 'success': False}, status=400)

# api view for collecte form
logger = logging.getLogger(__name__)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_fiche_collecte(request):
    """Créer une fiche de collecte avec gestion complète des erreurs"""
    # ✅ DEBUG : Afficher les données reçues
    #print("📥 Données reçues:")
    #print(json.dumps(request.data, indent=2, ensure_ascii=False))
    serializer = FicheCollecteSerializer(data=request.data)

    if not serializer.is_valid():
        logger.error(f"Validation errors: {serializer.errors}")
        return Response({
            'success': False,
            'message': 'Données invalides',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            # Sauvegarder avec rollback automatique en cas d'erreur
            fiche = serializer.save()

            # Log de succès
            logger.info(f"Fiche {fiche.Numero_fiche_de_collecte} créée par {request.user}")

            return Response({
                'success': True,
                'message': 'Fiche de collecte créée avec succès',
                'data': {
                    'fiche_id': fiche.id,
                    'numero_fiche': fiche.Numero_fiche_de_collecte
                }
            }, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.exception(f"Error creating fiche: {str(e)}")
        return Response({
            'success': False,
            'message': 'Erreur lors de la création de la fiche',
            'errors': {'non_field_errors': [str(e)]}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# generate numero fiche collecte
@require_http_methods(["GET"])
def generate_fiche_collecte_number(request):
    """
    Générer un numéro de fiche de collecte basé sur l'arrondissement
    Format: RR-DDD-AAA-NNNN
    - RR: 2 premiers caractères de la région
    - DDD: 3 premiers caractères du département
    - AAA: 3 premiers caractères de l'arrondissement
    - NNNN: Numéro séquentiel sur 4 chiffres
    """
    arrondissement_id = request.GET.get('arrondissement_id')
    edit_mode = request.GET.get('edit_mode', 'false').lower() == 'true'
    fiche_id = request.GET.get('fiche_id')

    if not arrondissement_id:
        return JsonResponse({
            'error': 'L\'ID de l\'arrondissement est requis',
            'success': False
        }, status=400)

    try:
        arrondissement = get_object_or_404(Arrondissemements, pk=arrondissement_id)
        departement = arrondissement.departement
        region = departement.Region

        # Générer les codes
        region_code = region.Libelle[:2].upper()
        dept_code = departement.LibelleFR[:3].upper()
        arr_code = get_arrondissement_code(arrondissement.LibelleFR)

        # Préfixe du numéro
        prefix = f"{region_code}{dept_code}{arr_code}"

        # ✅ Utiliser un verrou pour éviter les doublons
        with transaction.atomic():
            # Trouver le dernier numéro avec ce préfixe
            # dans le cas ou edit mode est true on enleve la fiche de collecte du filter
            if edit_mode and fiche_id:
                last_collecte = Collectes.objects.filter(
                    Numero_fiche_de_collecte__startswith=prefix
                ).exclude(pk=fiche_id).select_for_update().order_by('-Numero_fiche_de_collecte').first()
            else:
                last_collecte = Collectes.objects.filter(
                    Numero_fiche_de_collecte__startswith=prefix
                ).select_for_update().order_by('-Numero_fiche_de_collecte').first()

            if last_collecte:
                # Extraire le numéro séquentiel
                last_number = last_collecte.Numero_fiche_de_collecte[-4:]
                try:
                    numero_sequence = int(last_number) + 1
                except ValueError:
                    numero_sequence = 1
            else:
                numero_sequence = 1

            numero_collecte = f"{prefix}{numero_sequence:04d}"

        return JsonResponse({
            'numero_collecte': numero_collecte,
            'region_id': region.id,
            'dpt_id': departement.id,
            'arrondissement_id': arrondissement.id,
            'region': region.Libelle,
            'departement': departement.LibelleFR,
            'arrondissement': arrondissement.LibelleFR,
            'sequence': numero_sequence,
            'success': True
        }, status=200)

    except Arrondissemements.DoesNotExist:
        return JsonResponse({
            'error': 'Arrondissement introuvable',
            'success': False
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'error': f'Erreur lors de la génération: {str(e)}',
            'success': False
        }, status=500)


def get_arrondissement_code(libelle: str) -> str:
    """
    Extrait le code AAA d'un arrondissement
    Exemple:
    - "Commune de BAMUSO" -> "BAM"
    - "YAOUNDE 3" -> "YAO"
    """
    if not libelle:
        return ""

    libelle = libelle.strip().upper()

    prefix = "COMMUNE DE "
    if libelle.startswith(prefix):
        libelle = libelle[len(prefix):].strip()

    return libelle[:3]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_fiche_collecte(request, fiche_id):
    """Récupérer une fiche de collecte pour modification"""
    try:
        fiche = get_object_or_404(Collectes, pk=fiche_id)
        serializer = FicheCollecteSerializer(fiche)

        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception(f"Error fetching fiche: {str(e)}")
        return Response({
            'success': False,
            'message': 'Erreur lors de la récupération de la fiche',
            'errors': {'non_field_errors': [str(e)]}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_fiche_collecte(request, fiche_id):
    """Mettre à jour une fiche de collecte"""
    try:
        fiche = get_object_or_404(Collectes, pk=fiche_id)

        # Utiliser partial=True pour PATCH (mise à jour partielle)
        partial = request.method == 'PATCH'

        serializer = FicheCollecteSerializer(
            fiche,
            data=request.data,
            partial=partial
        )

        if not serializer.is_valid():
            logger.error(f"Validation errors: {serializer.errors}")
            return Response({
                'success': False,
                'message': 'Données invalides',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            updated_fiche = serializer.save()

            logger.info(f"Fiche {updated_fiche.Numero_fiche_de_collecte} mise à jour par {request.user}")

            return Response({
                'success': True,
                'message': 'Fiche de collecte mise à jour avec succès',
                'data': {
                    'fiche_id': updated_fiche.id,
                    'numero_fiche': updated_fiche.Numero_fiche_de_collecte
                }
            }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception(f"Error updating fiche: {str(e)}")
        return Response({
            'success': False,
            'message': 'Erreur lors de la mise à jour de la fiche',
            'errors': {'non_field_errors': [str(e)]}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
