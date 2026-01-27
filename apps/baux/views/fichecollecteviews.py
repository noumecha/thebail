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


def transform_queryset_to_listable(q):
    listable = []
    for item in q:
        listable.append({
            "id": item.id,
            "name": str(item)
        })
    return listable

class FicheCollecteViewSet(ModelViewSet):
    queryset = FicheCollecte.objects.all()
    serializer_class = FicheCollecteSerializer
    permission_classes = [IsAuthenticated]

class FicheCollecteFormView(LoginRequiredMixin, TemplateView):
    template_name = "baux/forms/fiche_collecte_form.html"
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["normes"] = Normes.objects.all()
        context["type_constructions"] = TypeConstructions.objects.all()
        context["type_contrats"] = TypeContrats.objects.all()
        context["periodicite_reglements"] = PeriodiciteReglement.objects.all()
        context["exercices"] = Exercice.objects.all()
        context["locataires"] = Locataires.objects.all()
        context["immeubles"] = Immeubles.objects.all()
        context["recensements"] = Recensements.objects.all()
        context["non_mandatements"] = Non_Mandatement.objects.all()
        context["type_locations"] = TypeLocations.objects.all()
        context["statut_batisses"] = StatutBatisse.objects.all()
        context["revetement_interieures"] = RevetementInts.objects.all()
        context["revetement_exterieures"] = RevetementExts.objects.all()
        context["localisations"] = Localisation.objects.all()
        # iterable list
        context["devises"] = DEVISES
        context["structures"] = transform_queryset_to_listable(Structures.objects.all()[:30])
        context["administrations"] = transform_queryset_to_listable(Administrations.objects.all()[:30])
        context["bailleurs"] = transform_queryset_to_listable(Bailleurs.objects.all()[:30])
        context["pays"] = transform_queryset_to_listable(Pays.objects.all()[:30])
        context["regions"] = transform_queryset_to_listable(Regions.objects.all()[:30])
        context["departements"] = transform_queryset_to_listable(Departements.objects.all()[:30])
        context["arrondissements"] = transform_queryset_to_listable(Arrondissemements.objects.all()[:30])
        context["revetement_exts"] = transform_queryset_to_listable(RevetementExts.objects.all()[:30])
        context["revetement_ints"] = transform_queryset_to_listable(RevetementInts.objects.all()[:30])
        context["pieces"] = transform_queryset_to_listable(Pieces.objects.all())

        # Prepare element groups for the template
        elements = list(ElementDeDescription.objects.all())
        element_groups = []
        group = []
        for index, el in enumerate(elements, start=1):
            group.append({
                "id": el.pk,
                "libelle": str(el),
            })
            if index % 9 == 0 or index == len(elements):
                element_groups.append(group)
                group = []
        context["element_groups"] = element_groups

        context["api_url"] = "/api/fiches/"

        return context
