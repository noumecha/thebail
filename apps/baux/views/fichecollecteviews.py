from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from web_project import TemplateLayout
from ..models import *
from ..serializers.serializers import FicheCollecteSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class FicheCollecteViewSet(ModelViewSet):
    queryset = FicheCollecte.objects.all()
    serializer_class = FicheCollecteSerializer
    permission_classes = [IsAuthenticated]

class FicheCollecteFormView(LoginRequiredMixin, TemplateView):
    template_name = "baux/forms/fiche_collecte_form.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["administrations"] = Administrations.objects.all()
        context["structures"] = Structures.objects.all()
        context["normes"] = Normes.objects.all()
        context["type_constructions"] = TypeConstructions.objects.all()
        context["type_contrats"] = TypeContrats.objects.all()
        context["exercices"] = Exercice.objects.all()
        context["locataires"] = Locataires.objects.all()
        context["bailleurs"] = Bailleurs.objects.all()
        context["immeubles"] = Immeubles.objects.all()
        context["recensements"] = Recensements.objects.all()
        context["non_mandatements"] = Non_Mandatement.objects.all()
        context["type_locations"] = TypeLocations.objects.all()
        context["localisations"] = Localisation.objects.all()
        context["pays"] = Pays.objects.all()
        context["regions"] = Regions.objects.all()
        context["departements"] = Departements.objects.all()
        context["arrondissements"] = Arrondissemements.objects.all()
        context["revetement_exts"] = RevetementExts.objects.all()
        context["revetement_ints"] = RevetementInts.objects.all()
        context["element_descriptions"] = ElementDeDescription.objects.all()
        context["pieces"] = Pieces.objects.all()
        context["api_url"] = "/api/fiches/"
        return context
