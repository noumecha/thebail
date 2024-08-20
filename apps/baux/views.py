from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from web_project import TemplateLayout
from .forms import LocatairesForm, BailleursForm,LocalisationForm,ImmeublesForm,ContratsForm,OccupantsForm
from .models import Locataires, Bailleurs,Localisation,Arrondissemements,Pays,Normes,Immeubles,Contrats,Occupants

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

    """def post(self, request, *args, **kwargs):
        context = {}
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        form = OccupantsForm()
        OccupantsList = Occupants.objects.all()
        context['OccupantsList'] = OccupantsList
        if request.method == 'POST':
            if 'save' in request.POST:
                pk = request.POST.get('save')
                if not pk:
                    form = OccupantsForm(request.POST)
                else:
                    OccupantsnList = Occupants.objects.get(id=pk)
                    form = OccupantsForm(request.POST, instance=OccupantsList)
                if form.is_valid():
                    form.save()
                form = OccupantsForm()
            elif 'delete' in request.POST:
                pk = request.POST.get('delete')
                OccupantsList = Occupants.objects.get(id=pk)
                OccupantsList.delete()
            elif 'edit' in request.POST:
                pk = request.POST.get('edit')
                OccupantsList = Occupants.objects.get(id=pk)
                form = OccupantsForm(instance=OccupantsList)
        context['form'] = form
        return render(request, "baux/occupants_list.html",context)"""

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
        return render(request, 'baux/bailleur.html', context)

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

# contrat class new approach using Django CBGVs
"""class ContratCreateView(CreateView):
    model = Contrat
    form_class = ContratsForm
    template_name = 'baux/contrat.html'
    success_url = reverse_lazy('baux:contrat')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['contratList'] = Contrat.objects.all()
        context['form'] = ContratsForm(instance=self.object)
        return context"""

class ContratListView(ListView):
    model = Contrats
    template_name = 'baux/contrat_list.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['contratList'] = Contrats.objects.all()
        return context

class ContratUpdateView(UpdateView):
    model = Contrats
    form_class = ContratsForm
    template_name = 'baux/contrat.html'
    success_url = reverse_lazy('baux:contrat')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['contratList'] = Contrats.objects.all()
        context['form'] = ContratsForm(instance=self.object)
        return context

class ContratDeleteView(DeleteView):
    model = Contrats
    template_name = 'baux/contrat_delete.html'
    success_url = reverse_lazy('baux:contrat')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['contratList'] = Contrats.objects.all()
        return context

class ContratView(TemplateView):
    model = Contrats
    template_name = 'baux/contrat.html'
    #predefined functiion
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["contratList"] = Contrats.objects.all()
        context["form"] = ContratsForm()
        return context

    def post(self, request, *args, **kwargs):
        context = {}
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        form = ContratsForm()
        if request.method == 'POST':
            if 'save' in request.POST:
                form = ContratsForm(request.POST)
                if form.is_valid():
                    form.save()
                    form = ContratsForm()

            elif 'delete' in request.POST:
                pk = request.POST.get('delete')
                contratList = Contrats.objects.get(id=pk)
                contratList.delete()

            elif 'edit' in request.POST:
                pk = request.POST.get('edit')
                contratList = Contrats.objects.get(id=pk)
                form = ContratsForm(instance=contratList)

        context['form'] = form
        return render(request, 'baux/contrat.html', context)