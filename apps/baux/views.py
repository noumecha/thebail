from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from web_project import TemplateLayout
from .forms import LocatairesForm,AccessoiresForm, BailleursForm,LocalisationForm,ImmeublesForm,ContratsForm,OccupantsForm,Non_MandatementForm,AvenantsForm
from .models import Accessoires, Locataires, Bailleurs,Localisation,Arrondissemements,Pays,Normes,Immeubles,Contrats,Occupants,Non_Mandatement,Avenants

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

#occupants classes : 
class OccupantsDeleteView(DeleteView):
    model = Occupants
    template_name = 'baux/occupants_delete.html'
    success_url = reverse_lazy('baux:occupants_list')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["form"] = OccupantsForm()
        return context

class OccupantsView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        #A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["OccupantsList"] = Occupants.objects.all()
        pk = kwargs.get('pk', None)
        if pk:
            occupants = get_object_or_404(Occupants, pk=pk)
            context["form"] = OccupantsForm(instance=occupants)
        else:
            context["form"] = OccupantsForm()
        context["is_update"] = pk is not None
        return context
    
    def post(self, request, *args, **kwargs):
        occupants_form = OccupantsForm(request.POST)
        pk = kwargs.get('pk', None)
        if pk:
            occupants = get_object_or_404(Occupants, pk=pk)
            occupants_form = OccupantsForm(request.POST, instance=occupants)
        else:
            occupants_form = OccupantsForm(request.POST)
        if occupants_form.is_valid():
            occupants_form.save()
            return redirect('baux:occupants_list')
        else:
            context = self.get_context_data(pk=pk)
            context = self.get_context_data()
            context["form"] = occupants_form
            return self.render_to_response(context)

#localisation classes : 
class LocalisationDeleteView(DeleteView):
    model = Localisation
    template_name = 'baux/localisation_delete.html'
    success_url = reverse_lazy('baux:localisation_list')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["form"] = LocalisationForm()
        return context

class LocalisationView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        #A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["localisationList"] = Localisation.objects.all()
        pk = kwargs.get('pk', None)
        if pk:
            localisation = get_object_or_404(Localisation, pk=pk)
            context["form"] = LocalisationForm(instance=localisation)
        else:
            context["form"] = LocalisationForm()
        context["is_update"] = pk is not None
        return context

    def post(self, request, *args, **kwargs):
        localisation_form = LocalisationForm(request.POST)
        pk = kwargs.get('pk', None)
        if pk:
            localisation= get_object_or_404(Localisation, pk=pk)
            localisation_form = LocalisationForm(request.POST, instance=localisation)
        else:
            localisation_form = LocalisationForm(request.POST)
        if localisation_form.is_valid():
            localisation_form.save()
            return redirect('baux:localisation_list')
        else:
            context = self.get_context_data(pk=pk)
            context["form"] = localisation_form
            return self.render_to_response(context)

#locataire classes
class LocataireDeleteView(DeleteView):
    model = Locataires
    template_name = 'baux/locataire_delete.html'
    success_url = reverse_lazy('baux:locataire_list')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["form"] = LocatairesForm()
        return context

class LocataireView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        #A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["locatairesList"] = Locataires.objects.all()
        pk = kwargs.get('pk', None)
        if pk:
            locataire = get_object_or_404(Locataires, pk=pk)
            context["form"] = LocatairesForm(instance=locataire)
        else:
            context["form"] = LocatairesForm()
        context["is_update"] = pk is not None
        return context

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk:
            locataire = get_object_or_404(Locataires, pk=pk)
            locataire_form = LocatairesForm(request.POST, request.FILES, instance=locataire)
        else:
            locataire_form = LocatairesForm(request.POST, request.FILES)
        if locataire_form.is_valid():
            locataire_form.save()
            return redirect('baux:locataire_list')
        else:
            context = self.get_context_data(pk=pk)
            context["form"] = locataire_form
            return self.render_to_response(context)

#bailleur classes 
class BailleurDeleteView(DeleteView):
    model = Bailleurs
    template_name = 'baux/bailleur_delete.html'
    success_url = reverse_lazy('baux:bailleur_list')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["form"] = BailleursForm()
        return context

class BailleurView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        #A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["BailleursList"] = Bailleurs.objects.all()
        pk = kwargs.get('pk', None)
        if pk:
            bailleur = get_object_or_404(Bailleurs, pk=pk)
            context["form"] = BailleursForm(instance=bailleur)
        else:
            context["form"] = BailleursForm()
        context["is_update"] = pk is not None
        return context

    def post(self, request, *args, **kwargs):
        bailleur_form = BailleursForm(request.POST)
        pk = kwargs.get('pk', None)
        if pk:
            bailleur = get_object_or_404(Bailleurs, pk=pk)
            bailleur_form = BailleursForm(request.POST, instance=bailleur)
        else:
            bailleur_form = BailleursForm(request.POST)

        if bailleur_form.is_valid():
            bailleur_form.save()
            return redirect('baux:bailleur_list')
        else:
            context = self.get_context_data(pk=pk)
            context["form"] = bailleur_form
            return self.render_to_response(context)

#immeuble classes
class ImmeubleDeleteView(DeleteView):
    model = Immeubles
    template_name = 'baux/immeuble_delete.html'
    success_url = reverse_lazy('baux:immeuble_list')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["form"] = ImmeublesForm()
        return context

class AccessoireDeleteView(DeleteView):
    model = Accessoires
    template_name = 'baux/accessoire_delete.html'
    success_url = reverse_lazy('baux:immeuble_accessoire')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["form"] = AccessoiresForm()
        return context

class AccessoireView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['accessoireList'] = Accessoires.objects.all()
        pk = kwargs.get('pk', None)
        if pk:
            accessoire = get_object_or_404(Accessoires, pk=pk)
            form = AccessoiresForm(instance=accessoire)
        else:
            form = AccessoiresForm()
        context["form"] = form
        context["is_update"] = pk is not None
        return context
    
    def post(self, request, *args, **kwargs):
        accessoire_form = AccessoiresForm(request.POST)
        pk = kwargs.get('pk', None)
        if pk:
            accessoire = get_object_or_404(Accessoires, pk=pk)
            accessoire_form = AccessoiresForm(request.POST, instance=accessoire)
        else:
            accessoire_form = AccessoiresForm(request.POST)

        if accessoire_form.is_valid():
            accessoire_form.save()
            return redirect('baux:immeuble_accessoire')
        else:
            context = self.get_context_data(pk=pk)
            context["form"] = accessoire_form
            return self.render_to_response(context)

class ImmeubleView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        #A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['immeubleList'] = Immeubles.objects.all()
        pk = kwargs.get('pk', None)
        if pk:
            immeuble = get_object_or_404(Immeubles, pk=pk)
            form = ImmeublesForm(instance=immeuble)
        else:
            form = ImmeublesForm()
        context["form"] = form
        context["is_update"] = pk is not None
        context["accessoire_form"] = AccessoiresForm()
        return context
    
    def post(self, request, *args, **kwargs):
        immeuble_form = ImmeublesForm(request.POST)
        accessoire_form = AccessoiresForm()
        pk = kwargs.get('pk', None)
        if pk:
            immeuble = get_object_or_404(Immeubles, pk=pk)
            immeuble_form = ImmeublesForm(request.POST, instance=immeuble)
        else:
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
            return redirect('baux:immeuble_list')
        else:
            context = self.get_context_data(pk=pk)
            context["form"] = immeuble_form
            context["accessoire_form"] = accessoire_form
            return self.render_to_response(context)

#Contrat Classes : 
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

#non_mandatement classes : 
class Non_MandatementDeleteView(DeleteView):
    model = Non_Mandatement
    template_name = 'baux/non_mandatement_delete.html'
    success_url = reverse_lazy('baux:non_mandatement_list')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["form"] = Non_MandatementForm()
        return context

class Non_MandatementView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["NonMandatementList"] = Non_Mandatement.objects.all()
        pk = kwargs.get('pk', None)
        if pk:
            non_mandatement = get_object_or_404(Non_Mandatement, pk=pk)
            context["form"] = Non_MandatementForm(instance=non_mandatement)
        else:
            context["form"] = Non_MandatementForm()
        context["is_update"] = pk is not None
        return context
    
    def post(self, request, *args, **kwargs):
        non_mandatement_form = Non_MandatementForm(request.POST)
        pk = kwargs.get('pk', None)
        if pk:
            non_mandatement = get_object_or_404(Non_Mandatement, pk=pk)
            non_mandatement_form = Non_MandatementForm(request.POST, instance=non_mandatement)
        else:
            non_mandatement_form = Non_MandatementForm(request.POST)
        if non_mandatement_form.is_valid():
            non_mandatement_form.save()
            return redirect('baux:non_mandatement_list')
        else:
            context = self.get_context_data(pk=pk)
            context["form"] = non_mandatement_form
            return self.render_to_response(context)

#aventnas classes : 
class AvenantsDeleteView(DeleteView):
    model = Avenants
    template_name = 'baux/avenant_delete.html'
    success_url = reverse_lazy('baux:avenant_list')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["form"] = AvenantsForm()
        return context

class AvenantsView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["avenantsList"] = Avenants.objects.all()
        pk = kwargs.get('pk', None)
        if pk:
            avenant = get_object_or_404(Avenants, pk=pk)
            context["form"] = AvenantsForm(instance=avenant)
        else:
            context["form"] = AvenantsForm()
        context["is_update"] = pk is not None
        return context
    
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk:
            avenant = get_object_or_404(Avenants, pk=pk)
            avenant_form = AvenantsForm(request.POST, instance=avenant)
        else:
            avenant_form = AvenantsForm(request.POST)

        if avenant_form.is_valid():
            avenant_form.save()
            return redirect('baux:avenant_list')
        else:
            context = self.get_context_data(pk=pk)
            context["form"] = avenant_form
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
    