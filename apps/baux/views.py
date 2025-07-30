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
            queryset = queryset.filter(q_objects)
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
        form = self.form_class(request.POST)
        if form.is_valid():
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

class OccupantsView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        #A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["OccupantsList"] = Occupants.objects.all()
        context["form"] = OccupantsForm()
        return context
    
    def post(self, request, *args, **kwargs):
        occupants_form = OccupantsForm(request.POST)
        if occupants_form.is_valid():
            occupants_form.save()
            return redirect('baux:occupants_list')
        else:
            context = self.get_context_data()
            context["form"] = occupants_form
            return self.render_to_response(context)

class LocalisationView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        #A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["localisationList"] = Localisation.objects.all()
        context["form"] = LocalisationForm()
        return context

    def post(self, request, *args, **kwargs):
        context = {}
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        form = LocalisationForm()
        localisationList = Localisation.objects.all()
        context['localisationList'] = localisationList
        if request.method == 'POST':
            if 'save' in request.POST:
                pk = request.POST.get('save')
                if not pk:
                    form = LocalisationForm(request.POST)
                else:
                    localisationList = Localisation.objects.get(id=pk)
                    form = LocalisationForm(request.POST, instance=localisationList)
                form.save()
                form = LocalisationForm()
            elif 'delete' in request.POST:
                pk = request.POST.get('delete')
                localisationList = Localisation.objects.get(id=pk)
                localisationList.delete()
            elif 'edit' in request.POST:
                pk = request.POST.get('edit')
                localisationList = Localisation.objects.get(id=pk)
                form = LocalisationForm(instance=localisationList)
        context['form'] = form
        return render(request, "baux/localisation.html",context)

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
class CollecteView(SessionWizardView):
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
class ImmeubleView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        #A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['immeubleList'] = Immeubles.objects.all()
        context["form"] = ImmeublesForm()
        context["accessoire_form"] = AccessoiresForm()
        return context
    
    def post(self, request, *args, **kwargs):
        immeuble_form = ImmeublesForm(request.POST)
        if immeuble_form.is_valid():
            immeuble_form.save()
            accessoires_data = request.POST.getlist('accessoires_data')
            for data in accessoires_data:
                libelle, quantite = data.split(':')
                Accessoires.objects.create(
                    Libelle=libelle,
                    Quantite=quantite,
                    Immeuble=Immeubles.objects.get(id=immeuble_form.instance.id)
                )
            return JsonResponse({
                'success': True,
                'message' : 'Immeuble enregistré avec succès'
            })
        else:
            return JsonResponse({
                'success': False,
                'message' : f"Erreur lors de l\'enregistrement de l'immeuble : {str(immeuble_form.errors)}",
            })

def get_immeubles(request):
    if request.method == 'GET':
        query = request.GET.get('searchFilter', '').strip()
        immeubles = Immeubles.objects.filter()
        # applying filters 
        if query:
            immeubles = immeubles.filter( 
                Q(Designation__icontains=query)
            )
        datas = render_to_string(
            'baux/partials/immeubles_partial.html',
            {'immeubles': immeubles}, 
            request=request
        )
        return JsonResponse({'success': True, 'html': datas})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def update_immeuble(request, **kwargs):
    pk = kwargs.get('pk', None)
    if pk:
        immeuble = get_object_or_404(Immeubles, pk=pk)
        immeuble_form = ImmeublesForm(request.POST, instance=immeuble)
        if immeuble_form.is_valid():
            immeuble = immeuble_form.save()
            return JsonResponse({
                'success': True,
                'message' : 'Immeuble mis à jour avec succès'
            })
        else:
            return JsonResponse({
                'success': False,
                'message' : f"Erreur lors de la mise à jour de l'immeuble : {str(immeuble_form.errors)}",
            })
    else:
        return JsonResponse({'success': False, 'message': 'Immeuble non trouvé'}, status=404)

def delete_immeuble(request, pk):
    try:
        immeuble = get_object_or_404(Immeubles, pk=pk)
        immeuble.delete()
        messages.success(request, "Immeuble supprimé avec succès!")
        return redirect('baux:immeuble_list')
    except Immeubles.DoesNotExist:
        messages.success(request, "Immeuble non trouvé !")
        return redirect('baux:immeuble_list')

def immeuble_form_view(request, pk=None):
    if pk:
        immeuble = get_object_or_404(Immeubles, pk=pk) if pk else None
        form = ImmeublesForm(instance=immeuble)
    else:
        form = ImmeublesForm()
    html = render_to_string('baux/forms/immeuble_form.html', {'form': form}, request=request)
    return JsonResponse({'success': True, 'html': html})

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
class RecensementView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['recensements'] = Recensements.objects.all()
        context["form"] = RecensementsForm()
        return context
    
    def post(self, request, *args, **kwargs):
        recensement_form = RecensementsForm(request.POST)
        if recensement_form.is_valid():
            recensement = recensement_form.save(commit=False)
            immeuble = recensement.Immeuble
            last_number = Recensements.objects.filter(Immeuble=immeuble).count()
            recensement.Numero = last_number + 1
            recensement_form.save()
            return JsonResponse({
                'success': True,
                'message' : 'Recensement enregistré avec succès'
            })
        else:
            return JsonResponse({
                'success': False,
                'message' : f"Erreur lors de l\'enregistrement du recensement : {str(recensement_form.errors)}",
            })

# update recensements
def update_recensements(request, **kwargs):
        pk = kwargs.get('pk', None)
        if pk:
            recensement = get_object_or_404(Recensements, pk=pk)
            recensement_form = RecensementsForm(request.POST, instance=recensement)
            if recensement_form.is_valid():
                recensement = recensement_form.save()
                return JsonResponse({
                    'success': True,
                    'message' : 'Recensement mis à jour avec succès'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message' : f"Erreur lors de la mise à jour du recensement : {str(recensement_form.errors)}",
                })
        else:
            return JsonResponse({'success': False, 'message': 'Recensement non trouvé'}, status=404)

# getting recensement datas
def get_recensements(request, **kwargs):
    if request.method == 'GET':
        query = request.GET.get('searchFilter', '').strip()
        recensements = Recensements.objects.filter()
        # applying filters 
        if query:
            recensements = recensements.filter( 
                Q(Immeuble__Designation__icontains=query) |
                Q(Type_immeuble__icontains=query) |
                Q(Type_mur__icontains=query)
            )
        datas = render_to_string(
            'baux/partials/immeuble_recensement_partial.html',
            {'recensements': recensements}, 
            request=request
        )
        return JsonResponse({'success': True, 'html': datas})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

# manage deletion 
def recensement_delete_view(request, pk):
    try:
        recensement = get_object_or_404(Recensements, pk=pk)
        recensement.delete()
        messages.success(request, "Recensement supprimé avec succès!")
        return redirect('baux:immeuble_recensement')
    except Recensements.DoesNotExist:
        messages.success(request, "Recensement non trouvé !")
        return redirect('baux:immeuble_recensement')

def recensement_form_view(request, pk=None):
    if pk:
        recensement = get_object_or_404(Recensements, pk=pk) if pk else None
        form = RecensementsForm(instance=recensement)
    else:
        form = RecensementsForm()
    html = render_to_string('baux/partials/recensement_form.html', {'form': form}, request=request)
    return JsonResponse({'success': True, 'html': html})

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
            contrat_form = ContratsForm(request.POST)

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
class Non_MandatementView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["NonMandatementList"] = Non_Mandatement.objects.all()
        context["form"] = Non_MandatementForm()
        return context
    
    def post(self, request, *args, **kwargs):
        non_mandatement_form = Non_MandatementForm(request.POST)
        if non_mandatement_form.is_valid():
            non_mandatement_form.save()
            return redirect('baux:non_mandatement_list')
        else:
            context = self.get_context_data()
            context["form"] = non_mandatement_form
            return self.render_to_response(context)

class AvenantsView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["avenantsList"] = Avenants.objects.all()
        context["form"] = AvenantsForm()
        return context
    
    def post(self, request, *args, **kwargs):
        avenants_form = AvenantsForm(request.POST)
        if avenants_form.is_valid():
            avenants_form.save()
            return redirect('baux:avenant_list')
        else:
            context = self.get_context_data()
            context["form"] = avenants_form
            return self.render_to_response(context)

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