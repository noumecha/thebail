from ..models import *
from ..serializers import ImmeubleSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
import logging
import json
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_immeuble_data(request, immeuble_id):
    try:
        immeuble = Immeubles.objects.get(pk=immeuble_id)
        serializer = ImmeubleSerializer(immeuble)
        # check if the immeuble already link to a collecte immeuble :
        is_linked_to_fiche = Collectes.objects.filter(Immeuble=immeuble_id).exists()
        #
        return Response({
            'success': True,
            'datas': serializer.data,
            'is_linked_to_fiche': is_linked_to_fiche
        }, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(f"Error fetching immeuble: {str(e)}")
        return Response({
            'success': False,
            'message': 'Erreur lors de la récupération de l\'immeuble',
            'errors': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_immeuble(request):
    """Créer un immeuble avec gestion complète des erreurs"""
    # ✅ DEBUG : Afficher les données reçues
    print("📥 Données reçues:")
    print(json.dumps(request.data, indent=2, ensure_ascii=False))
    serializer = ImmeubleSerializer(data=request.data)

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
            immeuble = serializer.save()

            # Log de succès
            logger.info(f"Immeuble {immeuble.Designation} créée par {request.user}")

            return Response({
                'success': True,
                'message': 'Immeuble créée avec succès',
                'data': {
                    'immeuble_id': immeuble.id,
                    'immeuble': immeuble.Designation
                }
            }, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.exception(f"Error creating immeuble: {str(e)}")
        return Response({
            'success': False,
            'message': 'Erreur lors de la création de l\'immeuble',
            'errors': {'non_field_errors': [str(e)]}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_immeuble(request, immeuble_id):
    """Mettre à jour un immeuble"""
    try:
        immeuble = get_object_or_404(Collectes, pk=immeuble_id)
        serializer = ImmeubleSerializer(
            immeuble,
            data=request.data,
        )

        if not serializer.is_valid():
            logger.error(f"Validation errors: {serializer.errors}")
            return Response({
                'success': False,
                'message': 'Données invalides',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            update_immeuble = serializer.save()
            logger.info(f"Fiche {update_immeuble.Designation} mise à jour par {request.user}")
            return Response({
                'success': True,
                'message': 'Immeuble mis à jour avec succès',
                'data': {
                    'immeuble_id': update_immeuble.id,
                    'immeuble': update_immeuble.Designation
                }
            }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception(f"Error updating immeuble: {str(e)}")
        return Response({
            'success': False,
            'message': 'Erreur lors de la mise à jour de l\'immeuble',
            'errors': {'non_field_errors': [str(e)]}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
