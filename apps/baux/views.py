from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from web_project import TemplateLayout
from .forms import LocatairesForm, BailleursForm,LocalisationForm,ImmeublesForm,ContratsForm,OccupantsForm,Dossiers_ReglementsForm,AvenantsForm
from .models import Locataires, Bailleurs,Localisation,Arrondissemements,Pays,Normes,Immeubles,Contrats,Occupants,Dossiers_Reglements,Avenants

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

class LocataireView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        #A function to init the global layout. It is defined in web_project/__init__.py file
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

    """def post(self, request, *args, **kwargs):
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
        return render(request, 'baux/bailleur_list.html', context)"""

class ImmeubleView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        #A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['immeubleList'] = Immeubles.objects.all()
        context["form"] = ImmeublesForm()
        return context

    def post(self, request, *args, **kwargs):
        context = {}
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        form = ImmeublesForm()
        immeubleList = Immeubles.objects.all()
        context['immeubleList'] = immeubleList
        if request.method == 'POST':
            if 'save' in request.POST:
                pk = request.POST.get('save')
                if not pk:
                    form = ImmeublesForm(request.POST)
                else:
                    immeubleList = Immeubles.objects.get(id=pk)
                    form = ImmeublesForm(request.POST, instance=immeubleList)
                if form.is_valid():
                    form.save()
                form = ImmeublesForm()
            elif 'delete' in request.POST:
                pk = request.POST.get('delete')
                immeubleList = Immeubles.objects.get(id=pk)
                immeubleList.delete()
            elif 'edit' in request.POST:
                pk = request.POST.get('edit')
                immeubleList = Immeubles.objects.get(id=pk)
                form = ImmeublesForm(instance=immeubleList)
        context['form'] = form
        return render(request, 'baux/immeuble.html', context)

class ContratView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["contratList"] = Contrats.objects.all()
        context["form"] = ContratsForm()
        return context

    def post(self, request, *args, **kwargs):
        contrat_form = ContratsForm(request.POST)
        if contrat_form.is_valid():
            contrat_form.save()
            return redirect('baux:contrat_list')
        else:
            context = self.get_context_data()
            context["form"] = contrat_form
            return self.render_to_response(context)

class Dossiers_ReglementsView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["dossiersReglementsList"] = Dossiers_Reglements.objects.all()
        context["form"] = Dossiers_ReglementsForm()
        return context
    
    def post(self, request, *args, **kwargs):
        doss_reglement_form = Dossiers_ReglementsForm(request.POST)
        if doss_reglement_form.is_valid():
            doss_reglement_form.save()
            return redirect('baux:dossier_reglement_list')
        else:
            context = self.get_context_data()
            context["form"] = doss_reglement_form
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