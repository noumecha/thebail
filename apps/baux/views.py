from django.shortcuts import render
from .forms import LocatairesForm, BailleursForm,LocalisationForm,ImmeublesForm,ContratsForm
from .models import Locataires, Bailleurs,Localisation,Arrondissemements,Pays,Normes,Immeubles,Contrats

# Create your views here.
def index (request):
    return render(request, "baux/index.html")

def Menuimmeuble (request):
    return render(request, "baux/layoutImmeuble.html")


def localisation (request):
    context = {}
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

def locataire(request):
    context = {}
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


def bailleur(request):
    context = {}
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

def immeuble (request):
    context = {}
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

def contrat (request):
    context = {}
    form = ContratsForm()
    contratList = Contrats.objects.all()
    context['contratList'] = contratList
    if request.method == 'POST':
        if 'save' in request.POST:
            pk = request.POST.get('save')
            if not pk:
                form = ContratsForm(request.POST)
            else:
                contratList = Contrats.objects.get(id=pk)
                form = ContratsForm(request.POST, instance=contratList)
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
    return render(request, 'baux/contrat.html',context)