from ..models import *
from ..serializers import ImmeubleSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

# getting immeuble data by his id
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_immeuble_data(request, immeuble_id):
    try:
        immeuble = Immeubles.objects.get(pk=immeuble_id)
        serializer = ImmeubleSerializer(immeuble)
        # check if the immeuble already link to a collecte fiche :
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
