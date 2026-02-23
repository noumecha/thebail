from django.http import JsonResponse
from django.db.models import Q
from django.views import View
from httpx import request
from ..models import *
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializers import BailleurSerializer
from django.db import transaction
import logging
import json

# api view for collecte form
logger = logging.getLogger(__name__)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_bailleur(request):
    """Créer une fiche de bailleur avec gestion complète des erreurs"""
    # ✅ DEBUG : Afficher les données reçues
    print("📥 Données reçues:")
    print(json.dumps(request.data, indent=2, ensure_ascii=False))
    serializer = BailleurSerializer(data=request.data)

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
