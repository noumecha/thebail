from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from web_project import TemplateLayout
from django.template.loader import render_to_string
from .models import *
from .forms import *
from django.http import HttpResponse
import xhtml2pdf.pisa as pisa
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.core.paginator import Paginator
from dal import autocomplete
from django.views.decorators.csrf import csrf_exempt
from django.forms import modelformset_factory
import json
from django.db import transaction
import traceback
import sys

# generic paritl view function :
def generic_partial_form_view(request, form_class, success_message):
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            instance = form.save()
            return JsonResponse({
                'success': True,
                'id': instance.id,
                'text': str(instance),
                'message': success_message,
            })
        else:
            html = render_to_string('baux/partials/form_template.html', {'form': form}, request=request)
            return JsonResponse({
                'success': False,
                'html': html,
                'message': 'Erreur lors de l\'enregistrement',
                'errors': form.errors,
            })
    else:
        form = form_class()
        html = render_to_string('baux/partials/form_template.html', {'form': form}, request=request)
        return JsonResponse({'html': html})

# usage : 
def revetementint_partial_form_view(request):
    return generic_partial_form_view(
        request,
        form_class=RevetementIntsForm,
        success_message='Revetement intérieur enregistré avec succès',
    )

def revetementext_partial_form_view(request):
    return generic_partial_form_view(
        request,
        form_class=RevetementExtsForm,
        success_message='Revetement extérieur enregistré avec succès',
    )

def exercice_partial_form_view(request):
    return generic_partial_form_view(
        request,
        form_class=ExercicesForm,
        success_message='Exercice enregistré avec succès',
    )

"""def bailleur_partial_form_view(request):
    return generic_partial_form_view(
        request,
        form_class=ExercicesForm,
        success_message='Exercice enregistré avec succès',
    )"""

#generic view for basic operation 
class BaseCRUDView(TemplateView):
    model = None
    form_class = None
    formset_class = None
    list_template = None
    list_route = None
    partial_template = None
    form_template = 'baux/partials/form_template.html'
    context_object_name = 'objects'
    search_fields = []
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context[self.context_object_name] = self.model.objects.all()
        context["form"] = self.form_class
        return context
    
    def get_queryset(self, search_query=None):
        queryset = self.model.objects.all().order_by('-Date_creation')
        if search_query and self.search_fields:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f"{field}__icontains": search_query})
            queryset = queryset.filter(q_objects).order_by('-Date_creation')
        return queryset[:100]
    
    def get_form_view(self, request, pk=None):
        instance = get_object_or_404(self.model, pk=pk) if pk else None
        form = self.form_class(instance=instance)
        formsets = {
            name: formset_class(instance=instance)
            for name, formset_class in getattr(self, "formsets_classes", {}).items()
        }
        html = render_to_string(self.form_template, {
            'form': form,
            "formsets": formsets
        }, request=request)
        return JsonResponse({'success': True, 'html':html})
    
    def get_list_data(self, request):
        search_query = request.GET.get('search', '').strip()
        queryset = self.get_queryset(search_query)
        paginator = Paginator(queryset, 25)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        html = render_to_string(
            self.partial_template, 
            {
                self.context_object_name: page_obj,
                'page_obj': page_obj,
                'paginator': paginator
            }, 
            request=request
        )
        return JsonResponse({
            'success': True, 
            'html': html,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            if self.form_class == RecensementsForm:
                recensement = form.save(commit=False)
                immeuble = recensement.Immeuble
                last_number = Recensements.objects.filter(Immeuble=immeuble).count()
                recensement.Numero = last_number + 1
                obj = form.save()
            else:
                obj = form.save()
                formsets_valid = True
                for name, formset_class in getattr(self, "formsets_classes", {}).items():
                    formset = formset_class(request.POST, instance=obj)
                    if formset.is_valid():
                        formset.save()
                    else:
                        formsets_valid = False

                if formsets_valid:
                    return JsonResponse({
                        'success': True,
                        'message': f'{self.model._meta.verbose_name} enregistré avec succès',
                        'data': {'id': obj.id, 'text': str(obj)}
                    })
            return JsonResponse({
                'success': True,
                'message': f'{self.model._meta.verbose_name} enregistré avec succès',
                'data': {
                    'id' : obj.id,
                    'text': str(obj)
                }
            })
        # error case
        html = render_to_string(self.form_template, {'form': form}, request=request)
        return JsonResponse({
            'success': False,
            'message': f'Erreur lors de l\'enregistrement',
            'errors' : form.errors,
            'html' : html
        })
    
    def update(self, request, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return JsonResponse({'success': False, 'message': 'Objet non trouvé'}, status=404)
        instance = get_object_or_404(self.model, pk=pk)
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save()
            formsets_valid = True
            for name, formset_class in getattr(self, "formsets_classes", {}).items():
                formset = formset_class(request.POST, instance=obj)
                if formset.is_valid():
                    formset.save()
                else:
                    formsets_valid = False
            if formsets_valid:
                return JsonResponse({
                    'success': True,
                    'message': f'{self.model._meta.verbose_name} enregistré avec succès',
                    'data': {'id': obj.id, 'text': str(obj)}
                })
            return JsonResponse({
                'success' : True,
                'message': f'{self.model._meta.verbose_name} mis à jour avec succès'
            })
        # error case
        html = render_to_string(self.form_template, {'form' : form}, request=request)#, "formset": formset
        return JsonResponse({
            'success' : False,
            'messages': f"Erreur lors de la mise à jour",
            'html' : html
        })
    
    def delete(self, request, pk):
        try:
            obj = get_object_or_404(self.model, pk=pk)
            obj.delete()
            messages.success(request, f"{self.model._meta.verbose_name} supprimé avec succès!")
            return redirect(f'baux:{self.list_route}')
        except Locataires.DoesNotExist:
            messages.success(request, f"{self.model._meta.verbose_name} non trouvé !")
            return redirect(f'baux:{self.list_route}')
    
    def partial_form_view(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST)
            if form.is_valid():
                obj = form.save()
                return JsonResponse({
                    'success' : True,
                    'id' : obj.id,
                    'text': str(obj)
                })
            html = render_to_string(self.form_template, {'form': form}, request=request)
            return JsonResponse({
                'success': False, 
                'html': html
            })
        else:
            form = self.form_class()
            html = render_to_string(self.form_template, {'form': form}, request=request)
            return JsonResponse({'html': html})

    def dispatch(self, request, *args, **kwargs):
        action = kwargs.pop('action', None)
        if action == 'list':
            return self.get_list_data(request)
        elif action == 'form':
            return self.get_form_view(request, kwargs.get('pk'))
        elif action == 'update':
            return self.update(request, **kwargs)
        elif action == 'delete':
            return self.delete(request, kwargs.get('pk'))
        elif action == 'partial_form':
            return self.partial_form_view(request)
        return super().dispatch(request, *args, **kwargs)
        

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
        
# for loading bailleur form in contrat form
def bailleur_partial_form_view(request):
    if request.method == "POST":
        form = BailleursForm(request.POST)
        if form.is_valid():
            bailleur = form.save()
            return JsonResponse({
                'success': True,
                'id': bailleur.id,
                'text': str(bailleur),
                'message': 'Bailleur enregistré avec succès',
            })
        else:
            html = render_to_string('baux/partials/form_template.html', {'form': form}, request=request)
            return JsonResponse({
                'success': False,
                'html': html,
                'message': f'Erreur lors de l\'enregistrement',
                'errors' : form.errors,
            })
    else:
        form = BailleursForm()
        html = render_to_string('baux/partials/form_template.html', {'form': form}, request=request)
        return JsonResponse({'html': html})
    
def typecontrat_partial_form_view(request):
    if request.method == "POST":
        form = TypeContratsForm(request.POST)
        if form.is_valid():
            typecontrat = form.save()
            return JsonResponse({
                'success': True,
                'id': typecontrat.id,
                'text': str(typecontrat),
                'message': 'Type de contrat enregistré avec succès',
            })
        else:
            html = render_to_string('baux/partials/form_template.html', {'form': form}, request=request)
            return JsonResponse({
                'success': False, 
                'html': html,
                'message': f'Erreur lors de l\'enregistrement',
                'errors' : form.errors,  
            })
    else:
        form = TypeContratsForm()
        html = render_to_string('baux/partials/form_template.html', {'form': form}, request=request)
        return JsonResponse({
            'html': html,
        })

# revetements views
class RevetementExtsView(BaseCRUDView):
    model = RevetementExts
    form_class = RevetementExtsForm
    list_route = 'revetementext_list'
    list_template = 'baux/revetementext_list.html'
    partial_template = 'baux/partials/revetementexts_partial.html'
    context_object_name = 'revetementexts'
    search_fields = ['libelle']

class RevetementIntsView(BaseCRUDView):
    model = RevetementInts
    form_class = RevetementIntsForm
    list_route = 'revetementint_list'
    list_template = 'baux/revetementint_list.html'
    partial_template = 'baux/partials/revetementints_partial.html'
    context_object_name = 'revetementints'
    search_fields = ['libelle']

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

# for modal purpose : when create immeuble inside a contrat
def immeuble_partial_form_view(request):
    if request.method == "POST":
        form = ImmeublesForm(request.POST)
        if form.is_valid():
            immeuble = form.save()
            return JsonResponse({
                'success': True,
                'message': "Immeuble ajouté avec succès",
                'id': immeuble.id,
                'text': str(immeuble)
            })
        else:
            html = render_to_string('baux/partials/immeuble_modal_form.html', {'form': form}, request=request)
            return JsonResponse({'success': False, 'html': html, 'errors': form.errors})
    else:
        form = ImmeublesForm()
        html = render_to_string('baux/partials/immeuble_modal_form.html', {'form': form}, request=request)
        return JsonResponse({'html': html})

# recensements views        
class RecensementView(BaseCRUDView):
    model = Recensements
    form_class = RecensementsForm
    list_route = 'recensement_list'
    list_template = 'baux/recensement_list.html'
    partial_template = 'baux/partials/recensements_partial.html'
    context_object_name = 'recensements'
    search_fields = ['Immeuble__Designation','Type_immeuble','Type_mur']

# Contrat Class and views : 
# autopcomplete task in partialing form 
class ServiceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Structures.objects.all()
        if self.q:
            qs = qs.filter(libelle__icontains=self.q)
        return qs
    
class StructureAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Structures.objects.all()
        if self.q:
            qs = qs.filter(LibelleFr__icontains=self.q)
        return qs

class AdminAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Administrations.objects.all()
        if self.q:
            qs = qs.filter(LibelleFr__icontains=self.q)
        return qs
    
class BailleurAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Bailleurs.objects.all()
        if self.q:
            qs = qs.filter(
                Q(Nom_prenom__icontains=self.q) | Q(Raison_social__icontains=self.q)
            )
        return qs
    
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
    
# for adding contrat type
class TypeContratView(BaseCRUDView):
    model = TypeContrats
    form_class = TypeContratsForm
    list_route = 'typecontrat_list'
    list_template = 'baux/typecontrat_list.html'
    partial_template = 'baux/partials/typecontrats_partial.html'
    context_object_name = 'typecontrats'
    search_fields = ['libelle', 'description']
    
# check if instace exist
def instanceExist(model, idEl, msg):
    instance = get_object_or_404(model, pk=idEl)
    if instance:
        return instance
    else:
        return JsonResponse({"success": False, "errors": msg}, status=400)

# collecte view
class CollecteView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["collecteList"] = Collectes.objects.all().order_by('-Date_creation')
        pieces = Pieces.objects.all()
        pk = kwargs.get('pk', None)
        if pk:
            collecte = get_object_or_404(Collectes, pk=pk)
            form = CollectesForm(instance=collecte)
        else:
            form = CollectesForm()
        context['avenants_formset'] = AvenantsFormSet(prefix="avenants")
        context['immeubles_formset'] = ImmeublesFormSet(prefix="immeubles")
        context['ayants_droits_formset'] = AyantDroitsFormSet(prefix="ayants_droits")
        context['occupants_residence_formset'] = OccupantsFormSet(prefix="occupants_residence")
        context['occupants_bureau_formset'] = OccupantBureauxFormSet(prefix="occupants_bureau")
        context['non_mandatements_formset'] = NonMandatementFormSet(prefix="non_mandatements")
        context["form"] = form
        context["pieces"] = pieces
        context["is_update"] = pk is not None
        return context

@csrf_exempt
def collecte_create(request):
    if request.method == "POST":
        collecte_form = CollectesForm(request.POST)

        if collecte_form.is_valid():
            #collecte = collecte_form.save()
            try:
                with transaction.atomic():
                    collecte = collecte_form.save()
                    bailleurInstance = get_object_or_404(Bailleurs, pk=collecte.Bailleur.pk)
                    print(collecte.Bailleur.pk)
                    # Sauvegarde des immeubles 
                    immeubles_json = request.POST.get("immeubles_data")
                    if immeubles_json:
                        try:
                            immeubles_data = json.loads(immeubles_json)
                            # immeuble validation : 
                            errors = []  # pour collecter toutes les errors
                            immeubles_valides = []

                            for idx, im in enumerate(immeubles_data):
                                designation = im.get("Designation")
                                construction = im.get("Construction")

                                # --- Vérification des champs requis ---
                                if not designation:
                                    errors.append(f"Immeuble {idx+1}: 'Designation' est requis.")
                                if not construction:
                                    errors.append(f"Immeuble {idx+1}: 'Type de Construction' est requis.")

                                # --- Vérification des doublons (par exemple même Designation + Ville) ---
                                if designation and Immeubles.objects.filter(
                                    Designation=designation,
                                    Ville=im.get("Ville")
                                ).exists():
                                    errors.append(
                                        f"Immeuble {idx+1}: déjà existant (Designation + Ville)."
                                    )

                                immeubles_valides.append(im)

                            # S'il y a des errors, on arrête et on retourne la réponse
                            if errors:
                                return JsonResponse({"success": False, "errors": errors}, status=400)

                            for im in immeubles_valides:
                                # getting proper instance base on id
                                typeconstruction = instanceExist(TypeConstructions, im.get("Construction"), "Type de Construction non existant")
                                norme = instanceExist(Normes, im.get("Norme"), "La norme cadastrale selectionné n'existe pas")
                                revInt = instanceExist(RevetementInts, im.get("Revetement_interieure"), "La revetement intérieure selectionné n'existe pas")
                                revExt = instanceExist(RevetementExts, im.get("Revetement_exterieure"), "La revetement extérieure selectionné n'existe pas")
                                region = instanceExist(Regions, im.get("region"), "La région selectionnée n'existe pas")
                                departement = instanceExist(Departements, im.get("departement"), "Le département selectionné n'existe pas")
                                arrondissement = instanceExist(Arrondissemements, im.get("arrondissement"), "L'arrondissemnt selectionnée n'existe pas")
                                # 
                                immeuble = Immeubles.objects.create(
                                    Collecte=collecte,
                                    Designation=im.get("Designation"),
                                    Construction=typeconstruction,
                                    Date_Construction=im.get("Date_Construction"),
                                    Nombre_de_pieces=im.get("Nombre_de_pieces"),
                                    Superficie_louer=im.get("Superficie_louer"),
                                    Norme=norme,
                                    Type_location=im.get("Type_location"),
                                    Type_localisation=im.get("Type_localisation"),
                                    pays=im.get("pays"),
                                    Ville=im.get("Ville"),
                                    Rue=im.get("Rue"),
                                    region=region,
                                    departement=departement,
                                    arrondissement=arrondissement,
                                    Quartier=im.get("Quartier"),
                                    Coordonee_gps=im.get("Coordonee_gps"),
                                    Situation_de_la_batisse=im.get("Situation_de_la_batisse"),
                                    Revetement_interieure=revInt,
                                    Revetement_exterieure=revExt,
                                    observation=im.get("observation"),
                                )

                                # éléments dynamiques liés à l’immeuble
                                for el in im.get("elements", []):
                                    ImmeubleElement.objects.create(
                                        immeuble=immeuble,
                                        element_id=el.get("element_id"),
                                        statut=el.get("statut", False),
                                        nombre=el.get("nombre", 0),
                                    )
                        except json.JSONDecodeError:
                            return JsonResponse({"success": False, "errors": "Erreur lors du décodage des immeubles."}, status=400)

                    # Traitement des ayants droits
                    ayants_droits_json = request.POST.get('ayants_droits_data')
                    if ayants_droits_json:
                        try:
                            ayants_droits = json.loads(ayants_droits_json)

                            for ad in ayants_droits:
                                Ayant_droits.objects.create(
                                    Bailleur=collecte.Bailleur.pk,
                                    Nom_Prenom=ad.get('Nom_Prenom'),
                                    Contact=ad.get('Contact'),
                                    Reference_Grosse=ad.get('Reference_Grosse'),
                                    Date_prise_effet_grosse=ad.get('Date_prise_effet_grosse'),
                                    Reference_certificat_non_effet=ad.get('Reference_certificat_non_effet'),
                                    Date_prise_effet_certificat_non_effet=ad.get('Date_prise_effet_certificat_non_effet')
                                )
                        except json.JSONDecodeError:
                            return JsonResponse({"success": False, "errors": "Erreur lors du décodage des ayants droits."}, status=400)

                    # Traitement des avenants (données JSON depuis JS)
                    avenants_json = request.POST.get('avenants_data')
                    if avenants_json:
                        try:
                            avenants = json.loads(avenants_json)
                            for a in avenants:
                                # getting proper instance base on id
                                ancienbailleur = instanceExist(Bailleurs, a.get('ancienBailleur'), "Ancien Bailleur selectionné non existant")
                                nouveaubailleur = instanceExist(Bailleurs, a.get('nouveauBailleur'), "Nouveau Bailleur selectionné non existant")
                                # 
                                Avenants.objects.create(
                                    Collecte=collecte,
                                    Ref_Avenant=a.get('ref'),
                                    Date_Signature=a.get('dateSignature'),
                                    Date_effet=a.get('dateEffet'),
                                    Modification_apportee=a.get('modificationApportee'),
                                    Ancien_bailleur=ancienbailleur,
                                    Nouveau_bailleur=nouveaubailleur,
                                    Localite=a.get('localite'),
                                    Montant_TTC_Mensuel_ancien=a.get('montantAncien'),
                                    Montant_TTC_Mensuel_Nouveau=a.get('montantNouveau'),
                                    Attestion_domicilliation_bancaire_ancien=a.get('attestationAncien'),
                                    Attestion_domicilliation_bancaire_nouveau=a.get('attestationNouveau'),
                                    Duree_Contrat_Ancien=a.get('dureeAncien'),
                                    Duree_Contrat_Nouveau=a.get('dureeNouveau'),
                                )
                        except json.JSONDecodeError:
                            return JsonResponse({"success": False, "errors": "Erreur lors du décodage des avenants."}, status=400)

                    # traitement des nonmandatement 
                    nonmandatements_json = request.POST.get('nonmandatements_data')
                    if nonmandatements_json:
                        try:
                            nonmandatements = json.loads(nonmandatements_json)
                            for n in nonmandatements:
                                # getting proper instance base on id
                                exercice = instanceExist(Exercice, n.get('Exercice'), "Exercice selectionné non existant")
                                #
                                mois = n.get('mois', {})
                                Non_Mandatement.objects.create(
                                    Exercice=exercice,
                                    Loyer_Mensuel=n.get('Loyer_Mensuel'),
                                    Ref_Attestattion=n.get('Ref_Attestattion'),
                                    janvier=mois.get('janvier'),
                                    fevrier=mois.get('fevrier'),
                                    mars=mois.get('mars'),
                                    avril=mois.get('avril'),
                                    mai=mois.get('mai'),
                                    juin=mois.get('juin'),
                                    juillet=mois.get('juillet'),
                                    aout=mois.get('aout'),
                                    septembre=mois.get('septembre'),
                                    octobre=mois.get('octobre'),
                                    novembre=mois.get('novembre'),
                                    decembre=mois.get('decembre'),
                                    Montant_total_exercice=n.get('Montant_total_exercice'),
                                    Visa_budgétaire=n.get('Visa_budgétaire'),
                                    Ref_contrat_avenant=n.get('Ref_contrat_avenant'),
                                    Bailleur=collecte.Bailleur.pk
                                )
                        except json.JSONDecodeError:
                            return JsonResponse({"success": False, "errors": "Erreur lors du décodage des attestation de non mandatement."}, status=400)

                    # traitement des occupants
                    # residence
                    occupantsResidences_json = request.POST.get('occupantsResidences_data')
                    if occupantsResidences_json:
                        try:
                            occupantsResidences = json.loads(occupantsResidences_json)

                            for obj in occupantsResidences:
                                # getting proper instance base on id
                                tutelle = instanceExist(Administrations, obj.get('Administration_tutelle'), "Administration tutelle selectionné non existant")
                                #
                                Occupants.objects.create(
                                    Nom_Prenom = obj.get('Nom_Prenom'),
                                    Administration_tutelle = tutelle,
                                    Fonction = obj.get('Fonction'),
                                    Matricule = obj.get('Matricule'),
                                    NIU = obj.get('NIU'),
                                    Ref_ActeJuridique = obj.get('Ref_ActeJuridique'),
                                    Date_Signature_acte_juridique = obj.get('Date_Signature_acte_juridique'),
                                    Telephone = obj.get('Telephone'),
                                    Immeuble=immeuble,
                                )
                        except json.JSONDecodeError:
                            return JsonResponse({"success": False, "errors": "Erreur lors du décodage des occupants résidents."}, status=400)
                    
                    # bureau
                    occupantsBureaux_json = request.POST.get('occupantsBureaux_data')
                    if occupantsBureaux_json:
                        try:
                            occupantsBureaux = json.loads(occupantsBureaux_json)

                            for obj in occupantsBureaux:
                                # getting proper instance base on id
                                service = instanceExist(Structures, obj.get('Service'), "Service selectionné non existant")
                                administration = instanceExist(Administrations, obj.get('Administration_correspondante'), "Administration correspondante selectionnée non existant")
                                #
                                OccupantBureaux.objects.create(
                                    Service=service,
                                    Administration_correspondante=administration,
                                    Fonction=obj.get('Fonction'),
                                    Ref_ActeJuridique_attribution=obj.get('Ref_ActeJuridique_attribution'),
                                    Contact=obj.get('Contact'),
                                    Date_initial_acte_occupation=obj.get('Date_initial_acte_occupation'),
                                    Immeuble=immeuble,
                                )
                        except json.JSONDecodeError:
                            return JsonResponse({"success": False, "errors": "Erreur lors du décodage des occupants de bureaux"}, status=400)

                    # traitement des pièces collectés
                    pieces_json = request.POST.get('pieces_data')
                    if pieces_json:
                        try:
                            pieces_data = json.loads(pieces_json)
                            for p in pieces_data:
                                piece_id = p.get('piece_id')
                                statut = p.get('statut', False)
                                nombre = p.get('nombre', 0)

                                # Validation côté serveur (sécurité)
                                if statut and (not nombre or nombre <= 0):
                                    return JsonResponse({
                                        "success": False,
                                        "errors": f"La pièce {piece_id} est cochée mais sans nombre valide."
                                    }, status=400)

                                if statut or nombre > 0:
                                    PieceCollectes.objects.create(
                                        Collecte=collecte,
                                        Piece_id=piece_id,
                                        statut=statut,
                                        nombre=nombre
                                    )

                        except json.JSONDecodeError:
                            return JsonResponse({"success": False, "errors": "Erreur lors du décodage des pièces collectées."}, status=400)

                    return JsonResponse({"success": True, "message": "Fiche de collecte enregistrée avec succès !"})
            except Exception as e:
                # rollback automatique si exception
                exc_type, exc_obj, exc_tb = sys.exc_info()
                ligne = exc_tb.tb_lineno  # récupère le numéro de ligne exact
                erreur_complete = traceback.format_exc()  # stacktrace complet
                return JsonResponse({
                    "success": False,
                    "errors": str(e),
                    "line": ligne,
                    "trace": erreur_complete
                }, status=400)
        else:
            return JsonResponse({"success": False, "errors": collecte_form.errors}, status=400)

    return JsonResponse({"success": False, "message": "Méthode non autorisée."}, status=405)

# contrat view 
class ContratView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["contratList"] = Contrats.objects.all().order_by('-Date_creation')
        pk = kwargs.get('pk', None)
        if pk:
            contrat = get_object_or_404(Contrats, pk=pk)
            form = ContratsForm(instance=contrat)
        else:
            form = ContratsForm()
        context["form"] = form
        context["is_update"] = pk is not None
        return context

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk:
            contrat = get_object_or_404(Contrats, pk=pk)
            contrat_form = ContratsForm(request.POST, instance=contrat)
        else:
            contrat_form = ContratsForm(request.POST, request.FILES)

        if contrat_form.is_valid():
            contrat_form.save()
            return redirect('baux:contrat_list')
        else:
            context = self.get_context_data(pk=pk)
            context["form"] = contrat_form
            return self.render_to_response(context)

    def print_contrat(request, pk):
        # fetch content from db and load template context
        contrat = get_object_or_404(Contrats, pk=pk)
        context = {"contrat" : contrat}
        html = render_to_string("baux/docs/contrat_doc.html", context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="f"contrat_{contrat.Ref_contrat}".pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error generating PDF', status=500)
        return response

class ContratUpdateView(UpdateView):
    model = Contrats
    form_class = ContratsForm
    template_name = 'baux/contrat.html'
    success_url = reverse_lazy('baux:contrat_list')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["form"] = self.get_form()
        return context

class ContratDeleteView(DeleteView):
    model = Contrats
    template_name = 'baux/contrat_delete.html'
    success_url = reverse_lazy('baux:contrat_list')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["form"] = ContratsForm()
        return context

# Non-Mandatement Class and views :
class Non_MandatementView(BaseCRUDView):
    model = Non_Mandatement
    form_class = NonMandatementForm
    list_route = 'non_mandatement_list'
    list_template = 'baux/non_mandatement_list.html'
    partial_template = 'baux/partials/non_mandatements_partial.html'
    context_object_name = 'non_mandatements'
    search_fields = ['Avenant__Ref_Avenant']

class AvenantsView(BaseCRUDView):
    model = Avenants
    form_class = AvenantsForm
    list_route = 'avenant_list'
    list_template = 'baux/avenant_list.html'
    partial_template = 'baux/partials/avenants_partial.html'
    context_object_name = 'avenants'
    search_fields = ['Ref_Avenant']

class ConsultationView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["datas"] = []
        return context
    
class StatsView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["datas"] = []
        return context