from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib import messages
from web_project import TemplateLayout
from django.template.loader import render_to_string
from ..models import *
from ..forms import *
from .views_base import BaseCRUDView
from django.db.models import Q
from django.core.paginator import Paginator
from dal import autocomplete

# Create your views here.
def index (request):
    return render(request, "baux/index.html")

def Menuimmeuble (request):
    return render(request, "baux/layoutImmeuble.html")

class HomeView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

#occupant view
class ExercicesView(BaseCRUDView):
    model = Exercice
    form_class = ExercicesForm
    list_route = 'exercice_list'
    list_template = 'baux/exercice_list.html'
    partial_template = 'baux/partials/exercices_partial.html'
    context_object_name = 'exercices'
    search_fields = ["annee","LibelleFR"]

class OccupantsView(BaseCRUDView):
    model = Occupants
    form_class = OccupantsForm
    list_route = 'occupant_list'
    list_template = 'baux/occupant_list.html'
    partial_template = 'baux/partials/occupants_partial.html'
    context_object_name = 'occupants'
    search_fields = ['Nom_Prenom','Matricule']

#occupant view
class TypeConstructionsView(BaseCRUDView):
    model = TypeConstructions
    form_class = TypeConstructionsForm
    list_route = 'typeconstruction_list'
    list_template = 'baux/typeconstruction_list.html'
    partial_template = 'baux/partials/typeconstruction_partial.html'
    context_object_name = 'typeconstructions'
    search_fields = ['description','libelle']

#locatlisation view
class LocalisationView(BaseCRUDView):
    model = Localisation
    form_class = LocalisationForm
    list_route = 'localisation_list'
    list_template = 'baux/localisation_list.html'
    partial_template = 'baux/partials/localisations_partial.html'
    context_object_name = 'localisations'
    search_fields = ['Quartier','region__Libelle','departement__LibelleFR','arrondissement__LibelleFR','pays__LibelleFR']

# Element de description
class ElementDeDescriptionView(BaseCRUDView):
    model = ElementDeDescription
    form_class = ElementDeDescriptionForm
    list_route = 'elementdescription_list'
    list_template = 'baux/elementdescription_list.html'
    partial_template = 'baux/partials/elementdescriptions_partial.html'
    context_object_name = 'elementdescriptions'
    search_fields = ['libelle']

# Pieces jointes views
class PieceView(BaseCRUDView):
    model = Pieces
    form_class = PiecesForm
    list_route = 'piece_list'
    list_template = 'baux/piece_list.html'
    partial_template = 'baux/partials/pieces_partial.html'
    context_object_name = 'pieces'
    search_fields = ['libelle']

# locataires views
class LocataireView(BaseCRUDView):
    model = Locataires
    form_class = LocatairesForm
    list_route = 'locataire_list'
    list_template = "baux/locataire_list.html"
    partial_template = "baux/partials/locataires_partial.html"
    context_object_name = 'locataires'
    search_fields = ['Intitule', 'Nom_Prenom_Representant']

# all bailleur views management
class BailleurView(BaseCRUDView):
    model = Bailleurs
    form_class = BailleursForm
    list_route = 'bailleur_list'
    list_template = 'baux/bailleur_list.html'
    partial_template = 'baux/partials/bailleurs_partial.html'
    context_object_name = 'bailleurs'
    search_fields = ['Nom_prenom', 'Raison_social']
    formsets_classes = {
        "ayants_droits_formset": AyantDroitsFormSet,
        "non_mandatements_formset": NonMandatementFormSet,
    }

# immeuble views
class ImmeubleView(BaseCRUDView):
    model = Immeubles
    form_class = ImmeublesForm
    list_route = 'immeuble_list'
    list_template = 'baux/immeuble_list.html'
    partial_template = 'baux/partials/immeubles_partial.html'
    context_object_name = 'immeubles'
    search_fields = ['Designation']
    # Ajout des formsets spécifiques à cette vue
    formsets_classes = {
        "occupants_residence_formset": OccupantsFormSet,
        "occupants_bureau_formset": OccupantBureauxFormSet
    }

# recensements views
class RecensementView(BaseCRUDView):
    model = Recensements
    form_class = RecensementsForm
    list_route = 'recensement_list'
    list_template = 'baux/recensement_list.html'
    partial_template = 'baux/partials/recensements_partial.html'
    context_object_name = 'recensements'
    search_fields = ['Immeuble__Designation','Type_immeuble','Type_mur']

# getting localisation datas base on selected arrondissment
def get_localisation_datas(request):
    if request.method == 'GET':
        arrondissement_id = request.GET.get('arrondissement_id')
        if not arrondissement_id:
            return JsonResponse({'error': 'Aucun arrondissement selectionné'}, status=400)
        try:
            arrondissement = get_object_or_404(Arrondissemements, pk=arrondissement_id)
            departement = arrondissement.departement
            region = get_object_or_404(Regions, pk=departement.Region.id)
            dpt = get_object_or_404(Departements, pk=departement.id)
            #
            number = Immeubles.objects.filter(region=region, departement=departement, Collecte__isnull=False).count()
            numero = number + 1
            numero_collecte = f"{region.Libelle[:2]}-{dpt.LibelleFR[:3]}-{arrondissement.LibelleFR[:3]}-{numero:04d}"
            return JsonResponse({
                'region_id': region.id,
                'dpt_id' : dpt.id,
                'numero_collecte' : numero_collecte,
                'success': True
                }, safe=False, status=200)
        except (ValueError, Administrations.DoesNotExist):
            return JsonResponse({'error': 'Arrondissement selectionné incorrect' + ValueError, 'success': False}, status=400)
    return JsonResponse({'error': 'Invalid request', 'success': False}, status=400)

# getting agent name base on the selected or entry matricule
def get_agent_name(request):
    if request.method == 'GET':
        agent_id = request.GET.get('agent_id')
        if not agent_id:
            return JsonResponse({'error': 'Aucun locataire selectionné'}, status=400)
        try:
            agent_id = int(agent_id)
            agent = get_object_or_404(AgentCollecte, pk=agent_id)
            name = agent.Nom + " " + agent.Prenom
            return JsonResponse({'agent': name, 'success': True}, safe=False, status=200)
        except (ValueError, Administrations.DoesNotExist):
            return JsonResponse({'error': 'Matricule de l\'agent incorrect' + ValueError, 'success': False}, status=400)
    return JsonResponse({'error': 'Invalid request', 'success': False}, status=400)

# filtering structure base on administration
def get_structures(request):
    if request.method == 'GET':
        administration_id = request.GET.get('administration_id')
        if not administration_id:
            return JsonResponse({'error': 'Aucun locataire selectionné'}, status=400)
        try:
            administration_id = int(administration_id)
            structures = Structures.objects.filter(Administration=administration_id)[:20]  # Limit to 20 results for performance
            structure_list = [{'id': structure.id, 'text': structure.LibelleFr} for structure in structures]
            return JsonResponse(structure_list, safe=False)
        except (ValueError, Administrations.DoesNotExist):
            return JsonResponse({'error': 'ID du locataire incorrect'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)
