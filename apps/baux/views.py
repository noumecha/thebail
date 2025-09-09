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
                'text': str(bailleur)
            })
        else:
            html = render_to_string('baux/partials/form_template.html', {'form': form}, request=request)
            return JsonResponse({'success': False, 'html': html})
    else:
        form = BailleursForm()
        html = render_to_string('baux/partials/form_template.html', {'form': form}, request=request)
        return JsonResponse({'html': html})

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
            qs = qs.filter(name__icontains=self.q)
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
    

# collecte view
class CollecteView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["collecteList"] = Collectes.objects.all().order_by('-Date_creation')
        pk = kwargs.get('pk', None)
        if pk:
            collecte = get_object_or_404(Collectes, pk=pk)
            form = CollectesForm(instance=collecte)
        else:
            form = CollectesForm()
        context['formsets'] = {
            "avenants_formset": AvenantsFormSet,
            "immeubles_formset": ImmeublesFormSet,
            "bailleurs_formset": BailleursFormSet,
        }
        context["form"] = form
        context["is_update"] = pk is not None
        return context

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk:
            collecte = get_object_or_404(Contrats, pk=pk)
            collecte_form = CollectesForm(request.POST, instance=collecte)
        else:
            collecte_form = CollectesForm(request.POST, request.FILES)

        if collecte_form.is_valid():
            collecte_form.save()
            return redirect('baux:collecte_list')
        else:
            context = self.get_context_data(pk=pk)
            context["form"] = collecte_form
            return self.render_to_response(context)

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