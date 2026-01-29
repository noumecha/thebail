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


def transform_queryset_to_listable(q, id_field='id', name_field='__str__'):
    listable = []
    for item in q:
        if isinstance(item, str):  # Si c'est déjà une string (values_list flat)
            listable.append({"id": item, "name": item})
        # case where q is a tuple
        elif isinstance(item, tuple):
            listable.append({
                "id": item[0],
                "name": item[1]
            })
        else:  # Si c'est un objet model
            listable.append({
                "id": item.id,
                "name": str(item)
            })
    return listable

class FicheCollecteViewSet(ModelViewSet):
    queryset = Collectes.objects.all()
    serializer_class = FicheCollecteSerializer
    permission_classes = [IsAuthenticated]

class FicheCollecteFormView(LoginRequiredMixin, TemplateView):
    template_name = "baux/forms/fiche_collecte_form.html"
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # elements for selections in template
        context["immeubles"] = Immeubles.objects.all()
        context["occupants"] = Occupants.objects.all()
        context["occupantsbureaux"] = OccupantBureaux.objects.all()
        context["contrats"] = Contrats.objects.all()
        context["non_mandatements"] = Non_Mandatement.objects.all()
        context["bailleurs"] = transform_queryset_to_listable(Bailleurs.objects.all()[:30])

        # iterable list
        context["type_constructions"] = TypeConstructions.objects.all()
        context["type_contrats"] = TypeContrats.objects.all()
        context["periodicite_reglements"] = PeriodiciteReglement.objects.all()
        context["revetement_interieures"] = RevetementInts.objects.all()
        context["revetement_exterieures"] = RevetementExts.objects.all()
        context["statut_batisses"] = StatutBatisse.objects.all()
        context["type_locations"] = TypeLocations.objects.all()
        context["devises"] = DEVISES
        context["exercices"] = transform_queryset_to_listable(Exercice.objects.all()[:30])
        context["banques"] = transform_queryset_to_listable(Banques.objects.all()[:30])
        context["type_personnes"] = transform_queryset_to_listable(TYPE_PERSONNE)
        context["statut_bailleur"] = transform_queryset_to_listable(STATUT_BAILLEUR)
        context["agentcollectes"] = transform_queryset_to_listable(AgentCollecte.objects.all()[:30])
        context["matriculesagents"] = transform_queryset_to_listable(AgentCollecte.objects.values_list('Matricule', flat=True)[:30])
        context["structures"] = transform_queryset_to_listable(Structures.objects.all()[:30])
        context["administrations"] = transform_queryset_to_listable(Administrations.objects.all()[:30])
        context["pays"] = transform_queryset_to_listable(Pays.objects.all()[:30])
        context["regions"] = transform_queryset_to_listable(Regions.objects.all()[:30])
        context["departements"] = transform_queryset_to_listable(Departements.objects.all()[:30])
        context["arrondissements"] = transform_queryset_to_listable(Arrondissemements.objects.all()[:30])

        # months for non_mndatement template
        context["non_mandatement_months"] = [
            'janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin',
            'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre'
        ]

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

        # prepares pieces groups for the template
        pieces = list(Pieces.objects.all())
        piece_groups = []
        group = []
        for index, el in enumerate(pieces, start=1):
            group.append({
                "id": el.pk,
                "libelle": str(el),
            })
            if index % 9 == 0 or index == len(pieces):
                piece_groups.append(group)
                group = []
        context["piece_groups"] = piece_groups

        # api url for submission
        context["api_url"] = "/api/fiches/"

        return context
