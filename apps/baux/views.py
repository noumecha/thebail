from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from web_project import TemplateLayout
from django.template.loader import render_to_string
from django.template.loader import render_to_string
from .forms import LocatairesForm,TypeContratsForm, AccessoiresForm, BailleursForm,LocalisationForm,ImmeublesForm,ContratsForm,OccupantsForm,Non_MandatementForm,AvenantsForm
from .models import Accessoires,TypeContrats, Locataires, Bailleurs,Localisation,Immeubles,Contrats,Occupants,Non_Mandatement,Avenants, Structures, Administrations
from django.http import HttpResponse
import xhtml2pdf.pisa as pisa
from formtools.wizard.views import SessionWizardView

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

# locataire 
class LocataireView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["locatairesList"] = Locataires.objects.all()
        context["form"] = LocatairesForm()
        return context
    
    def post(self, request, *args, **kwargs):
        context = {}
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        #context["locatairesList"] = Locataires.objects.all()
        form = LocatairesForm()
        locatairesList = Locataires.objects.all()
        context['locatairesList'] = locatairesList
        if request.method == 'POST':
            if 'save' in request.POST:
                pk = request.POST.get('save')
                if not pk:
                    form = LocatairesForm(request.POST)
                else:
                    locatairesList = Locataires.objects.get(id=pk)
                    form = LocatairesForm(request.POST, instance=locatairesList)
                form.save()
                form = LocatairesForm()
            elif 'delete' in request.POST:
                pk = request.POST.get('delete')
                locatairesList = Locataires.objects.get(id=pk)
                locatairesList.delete()
            elif 'edit' in request.POST:
                pk = request.POST.get('edit')
                locatairesList = Locataires.objects.get(id=pk)
                form = LocatairesForm(instance=locatairesList)
        context['form'] = form
        return render(request, 'baux/locataire.html', context)

class BailleurView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        #A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["BailleursList"] = Bailleurs.objects.all()
        context["form"] = BailleursForm()
        return context

    def post(self, request, *args, **kwargs):
        bailleur_form = BailleursForm(request.POST)
        if bailleur_form.is_valid():
            bailleur_form.save()
            return redirect('baux:bailleur_list')
        else:
            context = self.get_context_data()
            context["form"] = bailleur_form
            return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = {}
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        form = BailleursForm()
        BailleursList = Bailleurs.objects.all()
        context['BailleursList'] = BailleursList
        if request.method == 'POST':
            if 'save' in request.POST:
                pk = request.POST.get('save')
                if not pk:
                    form = BailleursForm(request.POST)
                else:
                    BailleursList = Bailleurs.objects.get(id=pk)
                    form = BailleursForm(request.POST, instance=BailleursList)
                if form.is_valid():
                    form.save()
                form = BailleursForm()
            elif 'delete' in request.POST:
                pk = request.POST.get('delete')
                BailleursList = Bailleurs.objects.get(id=pk)
                BailleursList.delete()
            elif 'edit' in request.POST:
                pk = request.POST.get('edit')
                BailleursList = Bailleurs.objects.get(id=pk)
                form = BailleursForm(instance=BailleursList)
        context['form'] = form
        return render(request, 'baux/bailleur_list.html', context)

# for modal purpose        
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
            html = render_to_string('baux/partials/bailleur_modal_form.html', {'form': form}, request=request)
            return JsonResponse({'success': False, 'html': html})
    else:
        form = BailleursForm()
        html = render_to_string('baux/partials/bailleur_modal_form.html', {'form': form}, request=request)
        return JsonResponse({'html': html})

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
        accessoire_form = AccessoiresForm()
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
            return redirect('baux:immeuble_list')
        else:
            context = self.get_context_data()
            context["form"] = immeuble_form
            context["accessoire_form"] = accessoire_form
            return self.render_to_response(context)
        
class RecensementView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['immeubleList'] = Immeubles.objects.all()
        context["form"] = ImmeublesForm()
        return context
    
# for modal purpose        
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

#Contrat Class : 
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
        

# Non-Mandatement Class :
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