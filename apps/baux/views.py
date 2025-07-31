from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from web_project import TemplateLayout
from django.template.loader import render_to_string
from .forms import RecensementsForm, LocatairesForm,TypeContratsForm, AccessoiresForm, BailleursForm,LocalisationForm,ImmeublesForm,ContratsForm,OccupantsForm,Non_MandatementForm,AvenantsForm
from .models import Accessoires, Recensements,TypeContrats, Locataires, Bailleurs,Localisation,Immeubles,Contrats,Occupants,Non_Mandatement,Avenants, Structures, Administrations
from django.http import HttpResponse
import xhtml2pdf.pisa as pisa
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.db.models import Q

#generic view for basic operation 
class BaseCRUDView(TemplateView):
    model = None
    form_class = None
    list_template = None
    list_route = None
    partial_template = None
    form_template = 'baux/partials/form_template.html'
    context_object_name = 'objects'
    search_fields = []

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context[self.context_object_name] = self.model.objects.all()
        context["form"] = self.form_class
        return context
    
    def get_queryset(self, search_query=None):
        queryset = self.model.objects.all()
        if search_query and self.search_fields:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f"{field}__icontains": search_query})
            queryset = queryset.filter(q_objects).order_by('-Date_creation')
        return queryset
    
    def get_form_view(self, request, pk=None):
        instance = get_object_or_404(self.model, pk=pk) if pk else None
        form = self.form_class(instance=instance)
        html = render_to_string(self.form_template, {'form': form}, request=request)
        return JsonResponse({'success': True, 'html':html})
    
    def get_list_data(self, request):
        search_query = request.GET.get('search', '').strip()
        objects = self.get_queryset(search_query)
        html = render_to_string(self.partial_template, {self.context_object_name: objects}, request=request)
        return JsonResponse({'success':True, 'html':html})
    
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
            return JsonResponse({
                'success': True,
                'message': f'{self.model._meta.verbose_name} enregistré avec succès',
                'data': {
                    'id' : obj.id,
                    'text': str(obj)
                }
            })
        html = render_to_string(self.form_template, {'form': form}, request=request)
        return JsonResponse({
            'success': False,
            'message': f'Erreur lors de l\'enregistrement',
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
            return JsonResponse({
                'success' : True,
                'message': f'{self.model._meta.verbose_name} mis à jour avec succès'
            })
        html = render_to_string(self.form_template, {'form' : form}, request=request)
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

#locatlisation view
class LocalisationView(BaseCRUDView):
    model = Localisation
    form_class = LocalisationForm
    list_route = 'localisation_list'
    list_template = 'baux/localisation_list.html'
    partial_template = 'baux/partials/localisations_partial.html'
    context_object_name = 'localisations'
    search_fields = ['Quartier','region__Libelle','departement__LibelleFR','arrondissement__LibelleFR','pays__LibelleFR']

# for multi-step-form for collecting data        
FORMS = [
    ("step1", LocatairesForm),
    ("step2", AccessoiresForm),
    ("step3", BailleursForm),
]

TEMPLATES = {
    "0": "baux/step1.html",
    "1": "baux/step2.html",
    "2": "baux/step3.html",
}

temp_storage = FileSystemStorage(location='/tmp/wizard_files') # Choose an appropriate temporary directory
class CollecteView(SessionWizardView):
    file_storage = temp_storage 

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context = TemplateLayout.init(self, context)
        return context

    
    def done(self, form_list, **kwargs):
        # Combine form data here
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
        # Example: Save to database or perform processing
        print(data)
        return render(self.request, 'baux/done.html', {'data': data})

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
    
# immeuble views
class ImmeubleView(BaseCRUDView):
    model = Immeubles
    form_class = ImmeublesForm
    list_route = 'immeuble_list'
    list_template = 'baux/immeuble_list.html'
    partial_template = 'baux/partials/immeubles_partial.html'
    context_object_name = 'immeubles'
    search_fields = ['Designation']

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
# filtering structure base on administration
def get_structures(request):
    if request.method == 'GET':
        administration_id = request.GET.get('administration_id')
        if not administration_id:
            return JsonResponse({'error': 'Aucun locataire selectionné'}, status=400)
        try:
            administration_id = int(administration_id)
            structures = Structures.objects.filter(Administration=administration_id)
            structure_list = [{'id': structure.id, 'text': structure.LibelleFr} for structure in structures]
            return JsonResponse(structure_list, safe=False)
        except (ValueError, Administrations.DoesNotExist):
            return JsonResponse({'error': 'ID du locataire incorrect'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

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
    
# for adding contrat type
class TypeContratView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["typeContratList"] = TypeContrats.objects.all()
        pk = kwargs.get('pk', None)
        if pk:
            type_contrat = get_object_or_404(TypeContrats, pk=pk)
            form = TypeContratsForm(instance=type_contrat)
        else:
            form = TypeContratsForm()
        context["form"] = form
        context["is_update"] = pk is not None
        return context

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk:
            type_contrat = get_object_or_404(TypeContrats, pk=pk)
            type_contrat_form = TypeContratsForm(request.POST, instance=type_contrat)
        else:
            type_contrat_form = TypeContratsForm(request.POST)

        if type_contrat_form.is_valid():
            type_contrat_form.save()
            return redirect('baux:type_contrat_list')
        else:
            context = self.get_context_data(pk=pk)
            context["form"] = type_contrat_form
            return self.render_to_response(context)

def typecontrat_form_view(request):
    if request.method == "POST":
        form = TypeContratsForm(request.POST)
        if form.is_valid():
            typecontrat = form.save()
            return JsonResponse({
                'success': True,
                'id': typecontrat.id,
                'text': str(typecontrat)
            })
        else:
            html = render_to_string('baux/partials/type_contrat_form.html', {'form': form}, request=request)
            return JsonResponse({'success': False, 'html': html})
    else:
        form = TypeContratsForm()
        html = render_to_string('baux/partials/type_contrat_form.html', {'form': form}, request=request)
        return JsonResponse({'html': html})
    
class ContratView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["contratList"] = Contrats.objects.all()
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
        print(context['contrat'])
        html = render_to_string("baux/docs/contrat_doc.html", context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="f"contrat_{contrat.Ref_contrat}".pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error generating PDF', status=500)
        return response
        

# Non-Mandatement Class and views :
class Non_MandatementView(BaseCRUDView):
    model = Non_Mandatement
    form_class = Non_MandatementForm
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